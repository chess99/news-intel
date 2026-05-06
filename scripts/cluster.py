#!/usr/bin/env python3.11
# DEPRECATED: Was never wired into the main pipeline. Kept for reference only.
"""
cluster.py — 对 raw/YYYY/MM/DD/ 原文做事件聚合，合并同一事件的多个来源

用法:
    python3.11 scripts/cluster.py [--date YYYY-MM-DD]

输出: clusters/YYYY-MM-DD.json
降级: 如果聚合失败，每篇文章作为独立 cluster，pipeline 不中断。

依赖: digest.py 中的 call_minimax() 和 read_article()
"""
import sys, json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# 复用 digest.py 的 call_minimax 和 read_article（同目录）
sys.path.insert(0, str(Path(__file__).parent))
from digest import call_minimax, read_article  # noqa: E402

WORKDIR = Path(__file__).parent.parent
RAW_DIR = WORKDIR / "raw"
CLUSTERS_DIR = WORKDIR / "clusters"
CST = timezone(timedelta(hours=8))

SUMMARY_PROMPT = (
    "用一句话描述这篇文章报道的核心事件，不超过20字，"
    "只输出事件描述，不要标点以外的任何其他内容。"
)


def extract_event_summary(article_id: str, article: dict) -> tuple[str, str]:
    """返回 (article_id, event_summary)。失败时 summary 为空字符串。"""
    text = article.get("title", "") + "\n" + article.get("body", "")[:1000]
    result = call_minimax(SUMMARY_PROMPT + "\n\n文章内容：\n" + text)
    return article_id, result.strip()[:50] if result else ""


def _llm_group_batch(ids: list[str], summaries: list[str]) -> list[list[str]]:
    """
    对一批 (id, summary) 用 LLM 分组。
    返回 [[id,...], ...] 格式。
    任何解析失败都降级为每条独立。
    """
    if not ids:
        return []
    numbered = "\n".join(f"{i}: {s}" for i, (_, s) in enumerate(zip(ids, summaries)))
    prompt = (
        "以下是新闻摘要列表，请将报道同一事件的条目分组。\n"
        "输出严格 JSON 格式，每组是条目索引（从0开始）的数组，"
        "例如: [[0,2],[1],[3,4]]\n"
        "所有索引必须出现在某个组中，不能遗漏或重复。\n"
        "不要包含任何其他文字，只输出 JSON。\n\n"
        f"摘要列表：\n{numbered}"
    )
    response = call_minimax(prompt)
    try:
        groups_idx = json.loads(response)
        result: list[list[str]] = []
        used: set[int] = set()
        for group in groups_idx:
            valid_group = []
            for idx in group:
                if isinstance(idx, int) and 0 <= idx < len(ids) and idx not in used:
                    valid_group.append(ids[idx])
                    used.add(idx)
            if valid_group:
                result.append(valid_group)
        # 任何 missing index 成为独立 cluster
        for idx in range(len(ids)):
            if idx not in used:
                result.append([ids[idx]])
        return result
    except Exception:
        # JSON 解析失败：每条独立
        return [[id_] for id_ in ids]


def group_summaries_sliding_window(id_summary_map: dict) -> list[list[str]]:
    """
    用滑动窗口（每批 15 条，步长 10）分组，避免单次 mega-call 的
    positional bias 和 index 丢失问题。
    返回 [[id1, id2], [id3], ...] 形式的分组。
    """
    ids = list(id_summary_map.keys())
    summaries = list(id_summary_map.values())
    n = len(ids)
    if n == 0:
        return []
    if n <= 15:
        return _llm_group_batch(ids, summaries)

    preliminary_groups: list[list[str]] = []
    seen: set[str] = set()

    for start in range(0, n, 10):
        end = min(start + 15, n)
        batch_ids = ids[start:end]
        batch_summaries = summaries[start:end]

        # 只处理还没分配的
        unseen_pairs = [
            (bid, bsum) for bid, bsum in zip(batch_ids, batch_summaries)
            if bid not in seen
        ]
        if not unseen_pairs:
            continue

        sub_ids = [p[0] for p in unseen_pairs]
        sub_sums = [p[1] for p in unseen_pairs]
        groups = _llm_group_batch(sub_ids, sub_sums)
        for g in groups:
            preliminary_groups.append(g)
            seen.update(g)

    # 任何未分配的 id 成为独立 cluster
    for id_ in ids:
        if id_ not in seen:
            preliminary_groups.append([id_])

    return preliminary_groups


def main():
    parser = argparse.ArgumentParser(description="Cluster raw articles by event")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    args = parser.parse_args()

    today = datetime.now(CST)
    date_str = args.date or today.strftime("%Y-%m-%d")
    yyyy, mm, dd = date_str.split("-")

    raw_dir = RAW_DIR / yyyy / mm / dd
    if not raw_dir.exists():
        print(f"[WARN] raw 目录不存在: {raw_dir}，跳过聚合", file=sys.stderr)
        sys.exit(0)

    files = sorted(raw_dir.glob("*.md"))
    if not files:
        print(f"[WARN] raw 目录为空: {raw_dir}，跳过聚合", file=sys.stderr)
        sys.exit(0)

    print(f"[INFO] 日期: {date_str}，文章数: {len(files)}", file=sys.stderr)

    # 读取文章（复用 read_article）
    articles: dict[str, dict] = {}
    for f in files:
        articles[f.stem] = read_article(f)

    # Step 1: 并发提取 event summary，key 用文件名 stem（稳定 ID）
    print("[Step1] 提取事件摘要...", file=sys.stderr)
    id_summary: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(extract_event_summary, art_id, art): art_id
            for art_id, art in articles.items()
        }
        for future in as_completed(futures):
            art_id = futures[future]
            try:
                _, summary = future.result()
                id_summary[art_id] = summary
            except Exception as e:
                id_summary[art_id] = ""
                print(f"  [WARN] {art_id}: summary 提取失败: {e}", file=sys.stderr)

    print(f"  [OK] {sum(1 for s in id_summary.values() if s)} 条摘要提取成功", file=sys.stderr)

    # Step 2: 滑动窗口分组
    print("[Step2] 事件分组...", file=sys.stderr)
    try:
        groups = group_summaries_sliding_window(id_summary)
    except Exception as e:
        print(f"  [WARN] 分组失败，降级为独立 cluster: {e}", file=sys.stderr)
        groups = [[art_id] for art_id in articles.keys()]

    # 生成 cluster JSON
    clusters = []
    for i, group in enumerate(groups, 1):
        group_articles = []
        for art_id in group:
            if art_id not in articles:
                continue
            art = articles[art_id]
            group_articles.append({
                "file": str(RAW_DIR / yyyy / mm / dd / (art_id + ".md")),
                "source": art.get("source", ""),
                "title": art.get("title", ""),
                "url": art.get("url", ""),
                "lang": art.get("lang", ""),
                "category": art.get("category", ""),
            })
        if not group_articles:
            continue
        clusters.append({
            "event_id": f"{date_str}-{i:03d}",
            "event_summary": id_summary.get(group[0], ""),
            "article_count": len(group_articles),
            "articles": group_articles,
            "sources": list({a["source"] for a in group_articles}),
        })

    multi_source = sum(1 for c in clusters if c["article_count"] > 1)
    print(f"  [OK] {len(clusters)} clusters ({multi_source} 个多来源)", file=sys.stderr)

    output = {"date": date_str, "clusters": clusters}
    CLUSTERS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CLUSTERS_DIR / f"{date_str}.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[DONE] {len(clusters)} clusters → {out_path}", file=sys.stderr)
    print(str(out_path))


if __name__ == "__main__":
    main()
