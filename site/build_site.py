#!/usr/bin/env python3
"""
build_site.py — 将 report/*.md 转换为精美静态 HTML，输出到 site/out/

用法:
    python3 site/build_site.py

输出目录: site/out/ (GitHub Pages 根目录)
依赖: pip install markdown
"""
import re
import json
from pathlib import Path
from datetime import datetime

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("[WARN] markdown 库未安装，降级为纯文本输出。运行: pip install markdown")

SCRIPT_DIR = Path(__file__).parent
WORKDIR = SCRIPT_DIR.parent
REPORT_DIR = WORKDIR / "report"
OUT_DIR = SCRIPT_DIR / "out"

# ─────────────────────────── CSS ───────────────────────────

DESIGN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;0,700;1,400;1,600&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+SC:wght@400;600;700&display=swap');

:root {
  /* ── Surfaces ── */
  --bg:          #0e1117;
  --bg-card:     #161b27;
  --bg-hover:    #1c2333;
  --bg-sidebar:  #0b0f1a;

  /* ── Borders ── */
  --border:       #2a3040;
  --border-light: #1e2535;

  /* ── Typography — WCAG AA compliant ── */
  --text:         #f0f2f7;   /* primary:   15.6:1 on --bg */
  --text-sub:     #b8c0d0;   /* secondary:  7.2:1 on --bg */
  --text-muted:   #7a8699;   /* muted:      4.6:1 on --bg */
  --text-dim:     #4e5a6e;   /* dim labels: decorative only */

  /* ── Accent — electric blue ── */
  --accent:       #4f8ef7;   /* 4.8:1 on --bg */
  --accent-soft:  #3a6fd0;
  --accent-glow:  rgba(79, 142, 247, 0.10);
  --accent-line:  rgba(79, 142, 247, 0.30);

  /* ── Semantic ── */
  --red:          #f26b5e;
  --red-dim:      rgba(242, 107, 94, 0.12);
  --green:        #5cba7d;
  --amber:        #e8a44a;

  /* ── Header height (mobile) ── */
  --header-h: 40px;

  /* ── Fonts ── */
  --mono:  'JetBrains Mono', 'Courier New', monospace;
  --serif: 'Newsreader', 'Noto Serif SC', Georgia, serif;
  --sans:  -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.75;
  min-height: 100dvh;
  -webkit-font-smoothing: antialiased;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── LAYOUT ── */
.site-wrapper {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100dvh;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── HEADER ── */
.site-header {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 0 2rem;
  height: 52px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: rgba(14,17,23,0.95);
  backdrop-filter: blur(14px);
  z-index: 100;
}

.site-logo {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
  white-space: nowrap;
}

.site-tagline {
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}

.site-header-sep {
  width: 1px;
  height: 14px;
  background: var(--border);
}

.site-header-right {
  margin-left: auto;
  font-family: var(--mono);
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.1em;
}

/* ── SIDEBAR ── */
.sidebar {
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  padding: 1.5rem 0;
  position: sticky;
  top: 52px;
  height: calc(100dvh - 52px);
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar-section {
  padding: 0 1rem;
  margin-bottom: 1.5rem;
}

.sidebar-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.archive-list { list-style: none; }

.archive-item {
  border-bottom: 1px solid var(--border-light);
}

.archive-link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.25rem;
  text-decoration: none;
  color: var(--text-muted);
  font-size: 12px;
  transition: color 0.15s;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}

.archive-link:hover { color: var(--text-sub); }
.archive-link.active { color: var(--text); }

.archive-link.active .archive-dot {
  background: var(--accent);
  box-shadow: 0 0 6px rgba(79, 142, 247, 0.5);
}

.archive-link.active .archive-date { color: var(--accent); }

.archive-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--border);
  flex-shrink: 0;
  transition: all 0.15s;
}

.archive-date {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: color 0.15s;
}

.archive-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 11px;
}

/* ── MAIN CONTENT ── */
.main-content {
  padding: 2rem 3rem 4rem;
  overflow-x: hidden;
  max-width: 860px;
}

/* ── REPORT VIEW ── */
.report-view { display: none; }
.report-view.active { display: block; }

/* ── REPORT BODY ── */
.report-body h1 {
  font-family: var(--serif);
  font-size: 1.9rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin-bottom: 0.75rem;
  color: var(--text);
}

.report-body .report-intro {
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--text-muted);
  letter-spacing: 0.04em;
  padding: 0.65rem 1rem;
  border-left: 2px solid var(--accent-soft);
  background: var(--accent-glow);
  margin-bottom: 2.5rem;
  line-height: 1.7;
}

.report-body h2 {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 3rem 0 1.25rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
}

.report-body h3 {
  font-family: var(--serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text);
  margin: 2rem 0 0.55rem;
  line-height: 1.45;
  letter-spacing: -0.01em;
}

.report-body p {
  color: var(--text-sub);
  margin-bottom: 0.85rem;
  line-height: 1.9;
  font-size: 15px;
}

.report-body blockquote {
  border-left: 2px solid var(--accent-line);
  margin: 1.25rem 0;
  padding: 0.65rem 1.1rem;
  background: var(--accent-glow);
  font-style: italic;
  font-size: 14px;
}

.report-body blockquote p {
  color: var(--text-muted);
  margin: 0;
  line-height: 1.7;
}

.report-body strong {
  color: var(--text);
  font-weight: 600;
}

.report-body em {
  font-style: italic;
  color: var(--text-sub);
}

.report-body hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

.report-body ul, .report-body ol {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.report-body li {
  color: var(--text-sub);
  margin: 0.3rem 0;
  font-size: 15px;
  line-height: 1.8;
}

.report-body li strong { color: var(--text); }

.report-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0 1.75rem;
  font-size: 13.5px;
}

.report-body th {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  text-align: left;
  padding: 0.55rem 0.85rem;
  border-bottom: 1px solid var(--border);
  background: transparent;
}

.report-body td {
  padding: 0.55rem 0.85rem;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-sub);
  vertical-align: top;
  line-height: 1.65;
}

.report-body tr:hover td { background: var(--bg-hover); }

.report-body code {
  font-family: var(--mono);
  font-size: 12.5px;
  background: var(--bg-card);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid var(--border);
}

.report-body pre {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 1.1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 1.25rem 0;
}

.report-body pre code {
  background: none;
  border: none;
  padding: 0;
  font-size: 12.5px;
  color: var(--text-sub);
}

/* ── FOOTER ── */
.report-footer {
  margin-top: 4rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.06em;
  line-height: 1.9;
}

.report-footer a { color: var(--text-muted); text-decoration: none; }
.report-footer a:hover { color: var(--accent); }

/* ── WELCOME / EMPTY ── */
.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  color: var(--text-dim);
}

.welcome-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.25;
}

.welcome-text {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.1em;
}

/* ── COUNT BADGE ── */
.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mono);
  font-size: 9px;
  padding: 1px 5px;
  border: 1px solid var(--border);
  color: var(--text-muted);
  border-radius: 2px;
  letter-spacing: 0.04em;
}

/* ── DATE DISPLAY TOGGLE ── */
.mobile-date { display: none; }
.desktop-date { display: inline; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .site-wrapper { grid-template-columns: 1fr; }

  .site-header {
    padding: 0 1rem;
    height: var(--header-h);
    gap: 0.6rem;
  }
  .site-tagline,
  .site-header-sep { display: none; }
  .site-logo { font-size: 10px; }
  .site-header-right { font-size: 9px; }

  /* Sidebar → sticky date chip strip */
  .sidebar {
    position: sticky;
    top: var(--header-h);
    height: auto;
    border-right: none;
    border-bottom: 1px solid var(--border);
    padding: 0;
    background: rgba(11, 15, 26, 0.97);
    backdrop-filter: blur(12px);
    z-index: 90;
    overflow: hidden;
  }
  .sidebar-section { padding: 0; margin: 0; }
  .sidebar-label { display: none; }

  .archive-list {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
    gap: 0;
    padding: 0.5rem 1rem;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .archive-list::-webkit-scrollbar { display: none; }

  .archive-item {
    border-bottom: none;
    flex-shrink: 0;
  }

  .archive-link {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 0.3rem 0.65rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-right: 0.4rem;
    white-space: nowrap;
    min-width: 52px;
    background: transparent;
    transition: border-color 0.15s, background 0.15s;
  }
  .archive-link.active {
    border-color: var(--accent);
    background: var(--accent-glow);
  }
  .archive-link:hover { color: var(--text-sub); background: var(--bg-hover); }

  .archive-dot { display: none; }

  .archive-date {
    font-size: 11.5px;
    color: var(--text-muted);
    letter-spacing: 0;
    line-height: 1.2;
  }
  .archive-link.active .archive-date { color: var(--accent); }

  .desktop-date { display: none; }
  .mobile-date { display: inline; }

  .main-content {
    padding: 1.25rem 1rem 3rem;
    max-width: 100%;
  }

  .report-body h1 { font-size: 1.5rem; }
  .report-body h3 { font-size: 1.05rem; }
  .report-body p, .report-body li { font-size: 14.5px; }

  .report-body table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    font-size: 12px;
  }
}

/* ── ANIMATIONS ── */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.report-view.active { animation: fadeIn 0.2s ease-out; }

@media (prefers-reduced-motion: reduce) {
  .report-view.active { animation: none; }
}

/* ── PRINT ── */
@media print {
  .sidebar, .site-header { display: none; }
  .site-wrapper { grid-template-columns: 1fr; }
  .main-content { padding: 0; max-width: 100%; }
  body { background: white; color: black; }
}
"""

# ─────────────────────────── HTML TEMPLATES ───────────────────────────

def make_page_html(reports_data: list) -> str:
    """
    Single-page app with all reports embedded as data.
    reports_data: [{date, title, html_body, meta}, ...]
    """
    latest = reports_data[0] if reports_data else None

    # Build sidebar archive items
    archive_items = ""
    for r in reports_data:
        date_display = r["date"]
        # Short date for mobile chips: MM/DD
        parts = r["date"].split("-")
        date_short = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else r["date"]
        is_latest = r is latest
        active_cls = " active" if is_latest else ""
        archive_items += f"""
        <li class="archive-item">
          <button class="archive-link{active_cls}" onclick="showReport('{r['date']}')" id="nav-{r['date']}">
            <span class="archive-dot"></span>
            <span class="archive-date desktop-date">{date_display}</span>
            <span class="archive-date mobile-date">{date_short}</span>
          </button>
        </li>"""

    # Build report views
    report_views = ""
    for r in reports_data:
        is_latest = r is latest
        active_cls = " active" if is_latest else ""
        report_views += f"""
    <div class="report-view{active_cls}" id="report-{r['date']}">
      <div class="report-body">
        {r['html_body']}
      </div>
      <div class="report-footer">
        <p>{r['footer']}</p>
      </div>
    </div>"""

    today_str = datetime.now().strftime("%Y-%m-%d")
    count = len(reports_data)

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="科技资讯日报 — 每日 AI 与科技深度资讯，批判性分析">
  <title>科技资讯日报 — INTEL DAILY</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style>{DESIGN_CSS}</style>
</head>
<body>
  <div class="site-wrapper">

    <!-- HEADER -->
    <header class="site-header">
      <span class="site-logo">Intel Daily</span>
      <span class="site-header-sep"></span>
      <span class="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
      <span class="site-header-right" id="current-date-display">{today_str}</span>
    </header>

    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-section">
        <div class="sidebar-label">归档 <span class="count-badge">{count}</span></div>
        <ul class="archive-list">
          {archive_items}
        </ul>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main-content">
      {report_views if report_views else '<div class="welcome-screen"><div class="welcome-icon">—</div><div class="welcome-text">暂无日报数据</div></div>'}
    </main>

  </div>

  <script>
    function showReport(date) {{
      // Hide all
      document.querySelectorAll('.report-view').forEach(el => {{
        el.classList.remove('active');
      }});
      document.querySelectorAll('.archive-link').forEach(el => {{
        el.classList.remove('active');
      }});

      // Show target
      const target = document.getElementById('report-' + date);
      const nav = document.getElementById('nav-' + date);
      if (target) target.classList.add('active');
      if (nav) nav.classList.add('active');

      // Update header date
      document.getElementById('current-date-display').textContent = date;

      // Update URL hash
      history.replaceState(null, '', '#' + date);

      // Scroll main to top
      document.querySelector('.main-content').scrollTop = 0;
    }}

    // Handle direct URL hash on load
    (function() {{
      const hash = window.location.hash.replace('#', '');
      if (hash && document.getElementById('report-' + hash)) {{
        showReport(hash);
      }}
    }})();
  </script>
</body>
</html>"""


# ─────────────────────────── MARKDOWN PROCESSING ───────────────────────────

def process_markdown(md_text: str) -> str:
    """Convert markdown to HTML with enhanced styling."""
    if not HAS_MARKDOWN:
        escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre>{escaped}</pre>"

    html = md_lib.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "attr_list"]
    )
    return html


def extract_meta(md_text: str, date_str: str) -> dict:
    """Extract metadata from report markdown."""
    lines = md_text.strip().split("\n")

    # Extract h1 title (first non-empty line starting with #)
    title = f"科技资讯日报 · {date_str}"
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            break

    # Extract meta line (blockquote after h1)
    meta = ""
    for line in lines[1:10]:
        stripped = line.strip()
        if stripped.startswith(">"):
            meta = stripped.lstrip("> ").strip()
            break

    # Short title for sidebar (strip emoji, keep date)
    title_short = re.sub(r'[^\w\s·年月日/\-]', '', title).strip()
    title_short = re.sub(r'\s+', ' ', title_short)
    # Just show the date portion for sidebar
    date_match = re.search(r'(\d{4}[年/\-]\d{1,2}[月/\-]\d{1,2})', title_short)
    if date_match:
        title_short = date_match.group(1)
    else:
        title_short = date_str

    # Footer line
    footer_match = re.search(r'📡\s*(.+)$', md_text, re.MULTILINE)
    footer = footer_match.group(1).strip() if footer_match else f"报告日期：{date_str}"
    # Clean up the footer for HTML
    footer = footer.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    return {
        "title": title,
        "title_short": title_short,
        "meta": meta,
        "footer": footer,
    }


def build_report_html(md_text: str, date_str: str) -> dict:
    """Build complete report data dict."""
    meta = extract_meta(md_text, date_str)

    # Remove the footer blockquote from body before rendering
    # (we render it separately in the template)
    body_text = re.sub(r'\n>\s*📡[^\n]*$', '', md_text.strip())

    html_body = process_markdown(body_text)

    return {
        "date": date_str,
        "title": meta["title"],
        "title_short": meta["title_short"],
        "meta": meta["meta"],
        "footer": meta["footer"],
        "html_body": html_body,
    }


# ─────────────────────────── MAIN ───────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # GitHub Pages: disable Jekyll processing
    (OUT_DIR / ".nojekyll").touch()

    reports = sorted(REPORT_DIR.glob("*.md"), reverse=True)
    if not reports:
        print("[WARN] 没有找到 report/*.md")

    reports_data = []
    for report_path in reports:
        date_str = report_path.stem
        try:
            md_text = report_path.read_text(encoding="utf-8")
            data = build_report_html(md_text, date_str)
            reports_data.append(data)
            print(f"  [OK] {date_str}")
        except Exception as e:
            print(f"  [WARN] 跳过 {report_path.name}: {e}")

    # Generate single-page app
    html = make_page_html(reports_data)
    out_path = OUT_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")

    print(f"\n[DONE] {len(reports_data)} 篇日报 → {out_path}")
    print(f"       预览: open {out_path}")


if __name__ == "__main__":
    main()
