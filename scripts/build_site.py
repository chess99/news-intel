#!/usr/bin/env python3.11
"""
build_site.py — 将 report/*.md 转换为静态 HTML，输出到 docs/

用法:
    python3.11 scripts/build_site.py

依赖（可选）: pip install markdown
如未安装 markdown 库，自动降级为 <pre> 格式输出。
"""
from pathlib import Path

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

WORKDIR = Path(__file__).parent.parent
REPORT_DIR = WORKDIR / "report"
DOCS_DIR = WORKDIR / "docs"

CSS = """
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Microsoft YaHei", sans-serif;
    max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem;
    color: #24292e; line-height: 1.7; background: #fff;
}
h1 { border-bottom: 2px solid #eaecef; padding-bottom: 0.5rem; font-size: 1.8rem; }
h2 { color: #444; margin-top: 2rem; font-size: 1.3rem; }
h3 { margin-top: 1.5rem; font-size: 1.1rem; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote {
    border-left: 4px solid #dfe2e5; margin: 0; padding: 0.5rem 1rem;
    color: #6a737d; background: #f6f8fa;
}
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
td, th { border: 1px solid #dfe2e5; padding: 6px 12px; text-align: left; }
th { background: #f6f8fa; }
code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
pre { background: #f6f8fa; padding: 1rem; border-radius: 4px; overflow-x: auto; }
pre code { background: none; padding: 0; }
.back { margin-bottom: 1.5rem; font-size: 0.9rem; }
hr { border: none; border-top: 1px solid #eaecef; margin: 1.5rem 0; }
ul { padding-left: 1.5rem; }
li { margin: 0.3rem 0; }
"""

INDEX_CSS = CSS + """
.report-list { list-style: none; padding: 0; }
.report-list li { padding: 0.5rem 0; border-bottom: 1px solid #eaecef; }
.report-list a { font-size: 1.05rem; }
.report-list .date { color: #6a737d; font-size: 0.85rem; margin-right: 0.5rem; }
"""


def md_to_html(md_text: str, title: str, back_link: str = "index.html") -> str:
    if HAS_MARKDOWN:
        body = md_lib.markdown(
            md_text,
            extensions=["tables", "fenced_code", "nl2br"]
        )
    else:
        # 基础 fallback
        escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        body = f"<pre>{escaped}</pre>"

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="back"><a href="{back_link}">← 返回目录</a></div>
  {body}
</body>
</html>"""


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    reports = sorted(REPORT_DIR.glob("*.md"), reverse=True)
    if not reports:
        print("[WARN] 没有找到 report/*.md，docs/ 将只有 index.html")

    pages = []
    for report_path in reports:
        date_str = report_path.stem
        try:
            md_text = report_path.read_text(encoding="utf-8")
            # 提取第一行 # 标题，去掉 emoji 得到简洁标题
            first_line = md_text.split("\n")[0].lstrip("# ").strip()
            title = first_line or f"科技资讯日报 · {date_str}"
            html = md_to_html(md_text, title)
            out_path = DOCS_DIR / f"{date_str}.html"
            out_path.write_text(html, encoding="utf-8")
            pages.append((date_str, title))
            print(f"  [OK] {out_path.name}")
        except Exception as e:
            print(f"  [WARN] 跳过 {report_path.name}: {e}")

    # 生成 index.html
    items = "\n".join(
        f'    <li><span class="date">{date}</span><a href="{date}.html">{title}</a></li>'
        for date, title in pages
    )
    index_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>科技资讯日报</title>
  <style>{INDEX_CSS}</style>
</head>
<body>
  <h1>📰 科技资讯日报</h1>
  <p>
    每日 AI 与科技深度资讯 ·
    <a href="https://github.com/chess99/news-intel">GitHub</a>
  </p>
  <ul class="report-list">
{items}
  </ul>
</body>
</html>"""
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"[DONE] {len(pages)} 篇日报 → {DOCS_DIR}/")


if __name__ == "__main__":
    main()
