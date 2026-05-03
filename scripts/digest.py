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
PROXY = "http://127.0.0.1:7890"

CST = timezone(timedelta(hours=8))

MINIMAX_API_KEY = os.environ.get(
    "MINIMAX_API_KEY",
    "sk-cp-qf8ALh36GGWaGpdojp2-5sDD00S0hpyZdwnG3H0dOB2c7vBzXXa9bAsGdrwCu69CkKI4_MvRoZOQxR4XgFEwykEfqwgLgomZ4OIq5ZWx4jWW4QrBX27_-uo"
)
MINIMAX_API_HOST = "https://api.minimaxi.com"
MODEL = "MiniMax-M2.7"

ANALYZE_PROMPT = """你是一位有15年经验的科技记者，同时具备软件工程背景。请对以下文章进行批判性分析。

【核心原则】
- 忠实还原，不强化断言：原文说"nearly"就写"nearly"，原文说"据报道"就保留，不得删除限定词
- 标注缺失信息：关键前提条件如果原文没说清楚，必须在"缺失信息"里标出
- 识别营销语言：区分事实陈述和PR措辞（"横空出世"/"颠覆"/"革命性"等）

【输出格式】严格按以下格式输出，不要有多余内容：

核心事件：[50字以内，忠实还原，保留限定词，不夸大不缩小]
原文引用：[直接引用原文最关键的1-2句，用引号括起，中英文均可]
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


def call_minimax(text: str) -> str:
    """调用 MiniMax API 分析文章，返回原始文本"""
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"{ANALYZE_PROMPT}\n\n---\n文章内容：\n{text[:5000]}"}
        ],
        "max_tokens": 600,
        "temperature": 0.2,
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
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  [ERROR] API call failed: {e}", file=sys.stderr)
        return ""


def parse_analysis(text: str) -> dict:
    """解析 API 输出为结构化字典"""
    result = {
        "core": "",
        "quote": "",
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
        if line.startswith("评分：") or line.startswith("评分:"):
            # 避免匹配"评分理由"
            raw_val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            # 只取第一个数字
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

SCORE_STARS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def main():
    parser = argparse.ArgumentParser(description="Analyze raw articles using LLM API")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--min-score", type=int, default=3, help="最低入选评分（默认3，减少低价值文章进入日报）")
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
    print(f"[INFO] 日期: {date_str}，找到 {len(files)} 篇文章，开始分析...", file=sys.stderr)

    results = []
    for i, filepath in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filepath.name}", file=sys.stderr)
        article = read_article(filepath)
        if not article["body"].strip():
            print(f"  [skip] 正文为空", file=sys.stderr)
            continue

        raw_analysis = call_minimax(article["body"])
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

    # 生成 digest 文件
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = DIGEST_DIR / f"{date_str}.md"

    lines = [
        f"# 科技资讯分析 · {date_str}",
        f"",
        f"> 共处理 {len(results)} 篇，入选 {len(filtered)} 篇（评分≥{args.min_score}）",
        f"> 生成时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST",
        f"",
        f"---",
        f"",
    ]

    # 按类别分组
    by_cat: dict[str, list] = {}
    for r in filtered:
        by_cat.setdefault(r["category"], []).append(r)

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
    print(str(digest_path))


if __name__ == "__main__":
    main()
