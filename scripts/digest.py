#!/usr/bin/env python3.11
"""
digest.py — 对 raw/YYYY/MM/DD/ 的原文逐篇调用 MiniMax API 进行批判性分析，
            汇总写入 digest/YYYY-MM-DD.md

用法：
    python3.11 scripts/digest.py [--date YYYY-MM-DD] [--min-score N]

每篇文章分析包含：
- 核心事件（忠实还原，保留限定词）
- 原文关键句引用
- 缺失信息标注
- 批判性判断（标题党识别、强度校准）
- 重要性评分

汇总文件按重要性排序，供龙虾直接用于生成日报。
龙虾层只需做最终编辑汇总，不承担分析工作。
"""
import os, sys, json, time, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import argparse
import urllib.request

WORKDIR = Path(__file__).parent.parent
RAW_DIR = WORKDIR / "raw"
DIGEST_DIR = WORKDIR / "digest"
PROXY = os.environ.get("HTTPS_PROXY", os.environ.get("HTTP_PROXY", ""))

CST = timezone(timedelta(hours=8))

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not MINIMAX_API_KEY:
    print("[ERROR] MINIMAX_API_KEY environment variable is not set.", file=sys.stderr)
    print("  Set it: export MINIMAX_API_KEY=your_key_here", file=sys.stderr)
    print("  Or copy .env.example to .env and fill in the values.", file=sys.stderr)
    sys.exit(1)
MINIMAX_API_HOST = os.environ.get("LLM_API_HOST", "https://api.minimaxi.com")
MODEL = os.environ.get("LLM_MODEL", "MiniMax-M2.7")

def build_analyze_prompt(kb_context: str = "") -> str:
    """构建分析 prompt，可选注入历史知识库上下文"""
    history_section = ""
    if kb_context:
        history_section = f"""
【历史知识库（过去30天高分事件，供关联分析）】
{kb_context}

"""
    return f"""你是一位有15年经验的科技记者，同时具备软件工程背景。{history_section}请对以下文章进行批判性分析。

【核心原则】
- 忠实还原，不强化断言：原文说"nearly"就写"nearly"，原文说"据报道"就保留，不得删除限定词
- 标注缺失信息：关键前提条件如果原文没说清楚，必须在"缺失信息"里标出
- 识别营销语言：区分事实陈述和PR措辞（"横空出世"/"颠覆"/"革命性"等）

【输出格式】严格按以下格式输出，不要有多余内容：

核心事件：[50字以内，忠实还原，保留限定词，不夸大不缩小]
原文引用：[直接引用原文最关键的1-2句，用引号括起，中英文均可]
历史关联：[与知识库中哪些事件有关？若无关联则写"无"]
底层驱动力：[为什么现在发生？市场动机/技术演进/商业逻辑，1-2句]
缺失信息：[原文未说但读者需要知道的关键前提或限制条件，若无则写"无"]
批判判断：[识别标题党/PR夸大/数据缺失/逻辑漏洞等问题，若无则写"叙述客观"]
背景补充：[结合业界知识补充1-2句有价值的背景，帮助读者理解实际意义]
评分：[1-5，整数]
评分理由：[一句话]

评分标准：
5=影响行业走向的重大突破或决策
4=值得关注的重要事件或产品发布
3=有价值的行业动态
2=一般资讯，价值有限
1=无关内容/纯广告/重复旧闻
"""


def call_minimax(prompt_or_text: str, article_text: str = "") -> str:
    """调用 MiniMax API，返回原始文本。

    两种调用方式：
    - call_minimax(full_prompt)          — prompt 已包含文章内容
    - call_minimax(prompt, article_text) — 分开传，函数自动拼接
    """
    if article_text:
        content = f"{prompt_or_text}\n\n---\n文章内容：\n{article_text[:5000]}"
    else:
        content = prompt_or_text

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": content}
        ],
        "max_tokens": 800,
        "temperature": 0.2,
    }).encode()

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        ctx = __import__("ssl")._create_unverified_context()
        if PROXY:
            proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
            opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        req = urllib.request.Request(
            f"{MINIMAX_API_HOST}/v1/chat/completions",
            data=payload,
            headers=headers,
            method="POST"
        )
        resp = opener.open(req, timeout=30)
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  [ERROR] API call failed: {e}", file=sys.stderr)
        return ""


def parse_analysis(text: str) -> dict:
    """解析 API 输出为结构化字典"""
    result = {
        "core": "",
        "quote": "",
        "history": "",
        "driver": "",
        "missing": "",
        "critique": "",
        "context": "",
        "score": 2,
        "score_reason": "",
        "raw": text,
    }

    field_map = {
        "核心事件": "core",
        "原文引用": "quote",
        "历史关联": "history",
        "底层驱动力": "driver",
        "缺失信息": "missing",
        "批判判断": "critique",
        "背景补充": "context",
        "评分理由": "score_reason",
    }

    for line in text.strip().split("\n"):
        line = line.strip()
        for prefix, key in field_map.items():
            if line.startswith(prefix + "：") or line.startswith(prefix + ":"):
                val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
                result[key] = val
                break
        if (line.startswith("评分：") or line.startswith("评分:")) and not line.startswith("评分理由"):
            raw_val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            # 只取第一个 1-5 数字（兼容 "4/5" 或 "4" 等格式）
            m = re.search(r"[1-5]", raw_val)
            if m:
                result["score"] = int(m.group())

    return result


def read_article(filepath: Path) -> dict:
    """读取文章 markdown，提取元数据和正文"""
    text = filepath.read_text(encoding="utf-8")

    meta = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            fm = text[3:end].strip()
            for line in fm.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            text = text[end + 3:].strip()

    return {
        "title": meta.get("title", filepath.stem),
        "url": meta.get("url", ""),
        "source": meta.get("source", ""),
        "category": meta.get("category", ""),
        "published": meta.get("published", "")[:10],
        "body": text[:5000],
        "filename": filepath.name,
    }


CAT_ZH = {
    "ai": "🤖 AI",
    "ai_official": "🏢 AI 官方",
    "ai_research": "🔬 AI 研究",
    "ai_newsletter": "📰 AI Newsletter",
    "ai_practitioner": "🛠️ AI 实践",
    "ai_zh": "🤖 中文 AI",
    "tech_startup": "🚀 科技创业",
    "consumer_tech": "📱 消费科技",
    "consumer_tech_zh": "📱 中文消费科技",
    "deep_tech": "🔬 深度技术",
    "deep_tech_research": "🎓 学术研究",
    "community": "👨‍💻 社区",
    "tech_business": "💼 科技商业",
    "open_source": "🌟 开源",
    "open_source_zh": "🌟 中文开源",
    "digital_life": "✨ 数字生活",
    "tech_culture": "🌐 科技文化",
    "engineering": "⚙️ 工程实践",
    "product": "🛍️ 产品发布",
    "startup": "🚀 创业",
    "platform": "🔧 平台动态",
}

SCORE_STARS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def load_kb_context() -> str:
    """读取知识库，返回注入 prompt 的历史事件文本（最多 50 条）"""
    kb_path = WORKDIR / "kb" / "events.jsonl"
    if not kb_path.exists():
        return ""
    events = []
    with kb_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    if not events:
        return ""
    events.sort(key=lambda r: r.get("date", ""), reverse=True)
    events = events[:50]
    return "\n".join(
        f"- [{r['date']}] {r['summary']} (来源: {', '.join(r.get('sources', []))})"
        for r in events
    )


def main():
    parser = argparse.ArgumentParser(description="Analyze raw articles using LLM API")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--min-score", type=int, default=3, help="最低入选评分（默认3）")
    args = parser.parse_args()

    today = datetime.now(CST)
    date_str = args.date or today.strftime("%Y-%m-%d")
    yyyy, mm, dd = date_str.split("-")

    raw_dir = RAW_DIR / yyyy / mm / dd
    if not raw_dir.exists():
        print(f"[WARN] 原文目录不存在: {raw_dir}，写入空 digest", file=sys.stderr)
        print(f"请先运行: python3.11 scripts/fetch.py --date {date_str}", file=sys.stderr)
        DIGEST_DIR.mkdir(parents=True, exist_ok=True)
        stub_path = DIGEST_DIR / f"{date_str}.md"
        stub_path.write_text(
            f"# 科技资讯分析 · {date_str}\n\n> 未运行 fetch.py，无文章数据。\n",
            encoding="utf-8"
        )
        print(str(stub_path))
        sys.exit(0)

    files = sorted(raw_dir.glob("*.md"))
    print(f"[INFO] 日期: {date_str}，找到 {len(files)} 篇文章，开始分析...", file=sys.stderr)

    # 加载历史知识库上下文
    kb_context = load_kb_context()
    if kb_context:
        kb_lines = kb_context.count("\n") + 1
        print(f"[INFO] 知识库注入: {kb_lines} 条历史事件", file=sys.stderr)
    analyze_prompt = build_analyze_prompt(kb_context)

    results = []
    for i, filepath in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filepath.name}", file=sys.stderr)
        article = read_article(filepath)
        if not article["body"].strip():
            print("  [skip] 正文为空", file=sys.stderr)
            continue

        raw_analysis = call_minimax(analyze_prompt, article["body"])
        if not raw_analysis:
            continue

        analysis = parse_analysis(raw_analysis)
        article["analysis"] = analysis
        results.append(article)

        score = analysis["score"]
        critique = analysis["critique"]
        print(f"  [{score}/5] {analysis['core'][:50]}", file=sys.stderr)
        if critique and critique != "叙述客观":
            print(f"  ⚠️  {critique[:60]}", file=sys.stderr)
        time.sleep(0.3)

    results.sort(key=lambda x: x["analysis"]["score"], reverse=True)
    filtered = [r for r in results if r["analysis"]["score"] >= args.min_score]

    print(f"\n[INFO] 分析完成，{len(filtered)}/{len(results)} 篇入选（评分≥{args.min_score}）", file=sys.stderr)

    # 生成 digest markdown 文件
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = DIGEST_DIR / f"{date_str}.md"

    lines = [
        f"# 科技资讯分析 · {date_str}",
        "",
        f"> 共处理 {len(results)} 篇，入选 {len(filtered)} 篇（评分≥{args.min_score}）",
        f"> 生成时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST",
        "",
        "---",
        "",
    ]

    # 按类别分组
    by_cat: dict[str, list] = {}
    for r in filtered:
        by_cat.setdefault(r["category"], []).append(r)

    priority_cats = [
        "ai_official", "ai", "ai_research", "ai_newsletter", "ai_practitioner", "ai_zh",
        "tech_startup", "tech_business", "consumer_tech", "consumer_tech_zh",
        "deep_tech", "open_source", "open_source_zh", "community", "deep_tech_research",
        "engineering", "product", "platform", "digital_life", "tech_culture",
    ]
    ordered_cats = [c for c in priority_cats if c in by_cat]
    ordered_cats += [c for c in by_cat if c not in ordered_cats]

    for cat in ordered_cats:
        items = by_cat[cat]
        cat_name = CAT_ZH.get(cat, cat)
        lines.append(f"## {cat_name}（{len(items)} 篇）")
        lines.append("")

        for r in items:
            a = r["analysis"]
            score = a["score"]
            stars = SCORE_STARS.get(score, "⭐" * score)

            lines.append(f"### {r['title']}")
            lines.append(f"**来源**: {r['source']} | **发布**: {r['published']} | **评分**: {stars} ({score}/5)")
            lines.append(f"**链接**: {r['url']}")
            lines.append("")

            lines.append(f"**核心**: {a['core']}")
            lines.append("")

            if a["quote"]:
                lines.append(f"**原文**: {a['quote']}")
                lines.append("")

            if a["history"] and a["history"] != "无":
                lines.append(f"**🔗 历史关联**: {a['history']}")
                lines.append("")

            if a["driver"]:
                lines.append(f"**💡 驱动力**: {a['driver']}")
                lines.append("")

            if a["missing"] and a["missing"] != "无":
                lines.append(f"**⚠️ 缺失信息**: {a['missing']}")
                lines.append("")

            if a["critique"] and a["critique"] != "叙述客观":
                lines.append(f"**🔍 批判**: {a['critique']}")
                lines.append("")

            if a["context"]:
                lines.append(f"**背景**: {a['context']}")
                lines.append("")

            lines.append("---")
            lines.append("")

    digest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[DONE] 分析文件已写入: {digest_path}", file=sys.stderr)

    # 写结构化 sidecar JSONL（供 kb_update.py 读取，无需解析 .md）
    sidecar_path = DIGEST_DIR / f"{date_str}.jsonl"
    with sidecar_path.open("w", encoding="utf-8") as f:
        for r in filtered:
            record = {
                "date": date_str,
                "event_id": f"{date_str}-{r['filename'][:3]}",
                "title": r["title"],
                "summary": r["analysis"]["core"],
                "score": r["analysis"]["score"],
                "score_reason": r["analysis"]["score_reason"],
                "sources": [r["source"]],
                "category": r["category"],
                "lang": r.get("lang", "unknown"),
                "url": r["url"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"[DONE] sidecar 已写入: {sidecar_path}", file=sys.stderr)

    print(str(digest_path))


if __name__ == "__main__":
    main()
