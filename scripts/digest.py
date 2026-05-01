#!/usr/bin/env python3.11
"""
digest.py — 对 raw/YYYY/MM/DD/ 的原文逐篇调用 MiniMax API 提炼，
            汇总写入 digest/YYYY-MM-DD.md

用法：
    python3.11 scripts/digest.py [--date YYYY-MM-DD]

每篇文章提炼为：
- 一句话核心观点（中文）
- 3-5 个要点（中文）
- 重要性评分 1-5

汇总文件按重要性排序，供龙虾直接用于生成日报。
"""
import os, sys, json, time, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import argparse
import urllib.request

WORKDIR = Path(__file__).parent.parent
RAW_DIR = WORKDIR / "raw"
DIGEST_DIR = WORKDIR / "digest"
PROXY = "http://127.0.0.1:7890"

CST = timezone(timedelta(hours=8))

MINIMAX_API_KEY = os.environ.get(
    "MINIMAX_API_KEY",
    "sk-cp-qf8ALh36GGWaGpdojp2-5sDD00S0hpyZdwnG3H0dOB2c7vBzXXa9bAsGdrwCu69CkKI4_MvRoZOQxR4XgFEwykEfqwgLgomZ4OIq5ZWx4jWW4QrBX27_-uo"
)
MINIMAX_API_HOST = "https://api.minimaxi.com"
MODEL = "MiniMax-M2.7"

EXTRACT_PROMPT = """你是一位科技资讯编辑，请对以下文章进行提炼分析。

要求：
1. 用一句话总结核心事件/观点（中文，≤50字）
2. 列出3-5个关键要点（中文，每点≤30字，用 • 开头）
3. 给出重要性评分（1-5分，5分最重要）
4. 评分依据：AI/大模型=5分，重大产品/商业事件=4分，行业动态=3分，普通资讯=2分，无关=1分

输出格式（严格按此格式）：
核心：[一句话总结]
要点：
• [要点1]
• [要点2]
• [要点3]
评分：[1-5]
"""


def call_minimax(text: str) -> dict:
    """调用 MiniMax API 提炼文章，返回结构化结果"""
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"{EXTRACT_PROMPT}\n\n文章内容：\n{text[:4000]}"}
        ],
        "max_tokens": 400,
        "temperature": 0.3,
    }).encode()

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        ctx = __import__("ssl")._create_unverified_context()
        proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
        opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
        req = urllib.request.Request(
            f"{MINIMAX_API_HOST}/v1/chat/completions",
            data=payload,
            headers=headers,
            method="POST"
        )
        resp = opener.open(req, timeout=30)
        data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        return parse_output(content)
    except Exception as e:
        print(f"  [ERROR] API call failed: {e}", file=sys.stderr)
        return {"core": "提炼失败", "points": [], "score": 1, "raw": ""}


def parse_output(text: str) -> dict:
    """解析 API 输出"""
    result = {"core": "", "points": [], "score": 2, "raw": text}

    lines = text.strip().split("\n")
    points = []
    in_points = False

    for line in lines:
        line = line.strip()
        if line.startswith("核心：") or line.startswith("核心:"):
            result["core"] = line.split("：", 1)[-1].split(":", 1)[-1].strip()
        elif line.startswith("要点"):
            in_points = True
        elif in_points and line.startswith("•"):
            points.append(line[1:].strip())
        elif line.startswith("评分：") or line.startswith("评分:"):
            try:
                score_str = line.split("：", 1)[-1].split(":", 1)[-1].strip()
                result["score"] = int(re.search(r"\d", score_str).group())
            except Exception:
                pass

    result["points"] = points
    return result


def read_article(filepath: Path) -> dict:
    """读取文章 markdown，提取元数据和正文"""
    text = filepath.read_text(encoding="utf-8")

    # 解析 frontmatter
    meta = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            fm = text[3:end].strip()
            for line in fm.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            text = text[end+3:].strip()

    # 取标题
    title = meta.get("title", filepath.stem)
    url = meta.get("url", "")
    source = meta.get("source", "")
    category = meta.get("category", "")
    published = meta.get("published", "")

    # 正文（RSS摘要 + 正文，合并用于提炼）
    body = text[:5000]

    return {
        "title": title,
        "url": url,
        "source": source,
        "category": category,
        "published": published[:10] if published else "",
        "body": body,
        "filename": filepath.name,
    }


CAT_ZH = {
    "ai": "🤖 AI",
    "tech_startup": "🚀 科技创业",
    "consumer_tech": "📱 消费科技",
    "deep_tech": "🔬 深度技术",
    "deep_tech_research": "🎓 学术研究",
    "community": "👨‍💻 社区",
    "tech_business": "💼 科技商业",
    "open_source": "🌟 开源",
    "digital_life": "✨ 数字生活",
    "tech_culture": "🌐 科技文化",
}


def main():
    parser = argparse.ArgumentParser(description="Digest raw articles using LLM API")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--min-score", type=int, default=2, help="最低入选评分（默认2）")
    args = parser.parse_args()

    today = datetime.now(CST)
    date_str = args.date or today.strftime("%Y-%m-%d")
    yyyy, mm, dd = date_str.split("-")

    raw_dir = RAW_DIR / yyyy / mm / dd
    if not raw_dir.exists():
        print(f"[ERROR] 原文目录不存在: {raw_dir}", file=sys.stderr)
        print(f"请先运行: python3.11 scripts/fetch.py --date {date_str}", file=sys.stderr)
        sys.exit(1)

    files = sorted(raw_dir.glob("*.md"))
    print(f"[INFO] 找到 {len(files)} 篇文章，开始提炼...", file=sys.stderr)

    results = []
    for i, filepath in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filepath.name}", file=sys.stderr)
        article = read_article(filepath)
        if not article["body"].strip():
            print(f"  [skip] 正文为空", file=sys.stderr)
            continue

        digest = call_minimax(article["body"])
        article["digest"] = digest
        results.append(article)
        print(f"  评分: {digest['score']} | 核心: {digest['core'][:40]}", file=sys.stderr)
        time.sleep(0.3)  # 避免限速

    # 按评分排序
    results.sort(key=lambda x: x["digest"]["score"], reverse=True)
    filtered = [r for r in results if r["digest"]["score"] >= args.min_score]

    print(f"\n[INFO] 提炼完成，{len(filtered)}/{len(results)} 篇入选（评分≥{args.min_score}）", file=sys.stderr)

    # 生成 digest 文件
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = DIGEST_DIR / f"{date_str}.md"

    lines = [
        f"# 科技资讯提炼 · {date_str}",
        f"",
        f"> 共处理 {len(results)} 篇，入选 {len(filtered)} 篇（评分≥{args.min_score}）",
        f"> 生成时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST",
        f"",
        f"---",
        f"",
    ]

    # 按类别分组输出
    by_cat: dict[str, list] = {}
    for r in filtered:
        cat = r["category"]
        by_cat.setdefault(cat, []).append(r)

    # AI 类别优先
    priority_cats = ["ai", "tech_startup", "tech_business", "consumer_tech",
                     "deep_tech", "open_source", "community", "deep_tech_research",
                     "digital_life", "tech_culture"]
    ordered_cats = [c for c in priority_cats if c in by_cat]
    ordered_cats += [c for c in by_cat if c not in ordered_cats]

    for cat in ordered_cats:
        items = by_cat[cat]
        cat_name = CAT_ZH.get(cat, cat)
        lines.append(f"## {cat_name}（{len(items)} 篇）")
        lines.append("")

        for r in items:
            d = r["digest"]
            score_stars = "⭐" * d["score"]
            lines.append(f"### {r['title']}")
            lines.append(f"**来源**: {r['source']} | **日期**: {r['published']} | **评分**: {score_stars} ({d['score']}/5)")
            lines.append(f"**链接**: {r['url']}")
            lines.append("")
            lines.append(f"**核心**: {d['core']}")
            lines.append("")
            if d["points"]:
                lines.append("**要点**:")
                for pt in d["points"]:
                    lines.append(f"- {pt}")
            lines.append("")
            lines.append("---")
            lines.append("")

    digest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[DONE] 提炼文件已写入: {digest_path}", file=sys.stderr)
    print(str(digest_path))  # stdout 输出路径，供调用方使用


if __name__ == "__main__":
    main()
