#!/usr/bin/env python3.11
"""
fetch.py — 抓取 RSS 信源，将每篇文章原文存档到 raw/YYYY/MM/DD/NNN-source-slug.md

用法：
    python3.11 scripts/fetch.py [--date YYYY-MM-DD] [--limit N]

每篇文章输出为独立 markdown 文件，包含元数据 frontmatter + 正文。
"""
import os, sys, re, json
import feedparser
import urllib.request, urllib.error, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
import threading
import argparse

WORKDIR = Path(__file__).parent.parent
sys.path.insert(0, str(WORKDIR))

from news_intel.config import load_sources
from news_intel.fetcher import source_slug
from news_intel.source_health import build_health_record
from news_intel.storage import write_json

SOURCES_FILE = WORKDIR / "sources" / "feeds.yaml"
RAW_DIR = WORKDIR / "raw"
STATE_DIR = WORKDIR / "state"
SOURCE_HEALTH_FILE = STATE_DIR / "source_health.json"
PROXY = os.environ.get("HTTPS_PROXY", os.environ.get("HTTP_PROXY", ""))
TIMEOUT = 20
MAX_PER_SOURCE = 5
MAX_CONTENT_CHARS = 8000  # 正文截断上限
MAX_ARTICLE_AGE_HOURS = 48  # 只保留 48 小时内的文章
MAX_RSS_WORKERS = 10        # 并发抓取 RSS 的线程数
MAX_CONTENT_WORKERS = 10    # 并发抓取全文的线程数

CST = timezone(timedelta(hours=8))

# 线程安全的计数器和锁
_idx_lock = threading.Lock()
_idx_counter = [0]


def _next_idx() -> int:
    with _idx_lock:
        _idx_counter[0] += 1
        return _idx_counter[0]


def slugify(text: str, max_len: int = 40) -> str:
    return source_slug(text, max_len=max_len)


def fetch_full_content(url: str) -> str:
    """抓取文章正文，返回清洗后的文本。失败时返回空字符串。"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        ctx = ssl._create_unverified_context()
        if PROXY:
            proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
            opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        req = urllib.request.Request(url, headers=headers)
        resp = opener.open(req, timeout=TIMEOUT)
        html = resp.read().decode("utf-8", errors="replace")

        # 优先找 <article> 或 <main>，否则用全页
        for tag in ["article", "main"]:
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.S | re.I)
            if m:
                html = m.group(1)
                break

        # 去掉脚本、样式
        html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
        html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:MAX_CONTENT_CHARS]
    except Exception:
        return ""


def fetch_feed(source: dict, date_str: str) -> list:
    """抓取单个 RSS 源，返回文章列表（已过滤 48h 外的旧文章）"""
    name = source["name"]
    url = source["url"]
    source["_fetch_error"] = ""
    effective_proxy = PROXY if source.get("use_proxy", True) else ""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NewsIntelBot/1.0)",
        "Accept": "application/rss+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
    }
    ctx = ssl._create_unverified_context()
    try:
        if effective_proxy:
            proxy_handler = urllib.request.ProxyHandler({"http": effective_proxy, "https": effective_proxy})
            opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        req = urllib.request.Request(url, headers=headers)
        resp = opener.open(req, timeout=TIMEOUT)
        content = resp.read()
    except ConnectionRefusedError:
        source["_fetch_error"] = f"proxy connection refused ({effective_proxy!r})"
        print(f"[WARN] {name}: 代理连接被拒绝 (HTTPS_PROXY={effective_proxy!r})，请检查代理设置", file=sys.stderr)
        return []
    except Exception as e:
        source["_fetch_error"] = str(e)
        print(f"[WARN] {name}: RSS fetch failed: {e}", file=sys.stderr)
        return []

    d = feedparser.parse(content)
    now = datetime.now(CST)
    articles = []
    for entry in d.entries[:MAX_PER_SOURCE]:
        pub = ""
        pub_dt = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                pub_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                pub = pub_dt.astimezone(CST).isoformat()
            except Exception:
                pass

        # 过滤 48 小时外的旧文章（无法解析发布时间的文章保留）
        if pub_dt is not None:
            age_hours = (now - pub_dt.astimezone(CST)).total_seconds() / 3600
            if age_hours > MAX_ARTICLE_AGE_HOURS:
                continue

        rss_summary = entry.get("summary", "") or entry.get("description", "") or ""
        rss_summary = re.sub(r"<[^>]+>", " ", rss_summary)
        rss_summary = re.sub(r"\s+", " ", rss_summary).strip()[:500]

        articles.append({
            "title": entry.get("title", "").strip(),
            "url": entry.get("link") or entry.get("id", ""),
            "rss_summary": rss_summary,
            "published": pub,
            "source": name,
            "lang": source["lang"],
            "category": source["category"],
        })
    return articles


def load_previous_source_health() -> dict:
    if not SOURCE_HEALTH_FILE.exists():
        return {}
    try:
        return json.loads(SOURCE_HEALTH_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_source_health(sources: list[dict], counts: dict[str, int]) -> None:
    previous = load_previous_source_health()
    now = datetime.now(CST).isoformat()
    health = {}
    for source in sources:
        count = counts.get(source["name"], 0)
        error = source.get("_fetch_error", "")
        status = "failed" if error else ("ok" if count > 0 else "empty")
        proxy_used = PROXY if source.get("use_proxy", True) else ""
        record = build_health_record(
            source=source,
            status=status,
            fetched_count=count,
            failure_reason=error,
            proxy_used=proxy_used,
            now=now,
            previous=previous.get(source["name"]),
        )
        health[source["name"]] = record.model_dump(mode="json")
    write_json(SOURCE_HEALTH_FILE, health)


def save_article(article: dict, out_dir: Path, idx: int) -> Path:
    """将文章保存为 markdown 文件，同时抓取正文"""
    url = article["url"]
    slug = slugify(article["title"])
    source_slug = slugify(article["source"], max_len=20)
    filename = f"{idx:03d}-{source_slug}-{slug}.md"
    filepath = out_dir / filename

    if filepath.exists():
        print(f"  [skip] {filename} (already exists)", file=sys.stderr)
        return filepath

    print(f"  [fetch] {article['title'][:60]}...", file=sys.stderr)
    content = fetch_full_content(url) if url else ""

    md = f"""---
title: "{article['title'].replace('"', "'")}"
source: {article['source']}
url: {url}
published: {article['published']}
lang: {article['lang']}
category: {article['category']}
fetched_at: {datetime.now(CST).isoformat()}
---

# {article['title']}

**来源**: {article['source']} | **发布**: {article['published'][:10] if article['published'] else '未知'} | **链接**: {url}

## RSS 摘要

{article['rss_summary'] or '（无摘要）'}

## 正文

{content or '（正文抓取失败，请访问原链接）'}
"""
    filepath.write_text(md, encoding="utf-8")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Fetch RSS articles to raw/")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--limit", type=int, default=None, help="每个源最多抓取篇数")
    args = parser.parse_args()

    today = datetime.now(CST)
    date_str = args.date or today.strftime("%Y-%m-%d")
    yyyy, mm, dd = date_str.split("-")

    out_dir = RAW_DIR / yyyy / mm / dd
    out_dir.mkdir(parents=True, exist_ok=True)

    sources = [s for s in load_sources(SOURCES_FILE) if s.get("enabled", True)]

    print(f"[INFO] 日期: {date_str}，信源数: {len(sources)}，输出目录: {out_dir}", file=sys.stderr)

    # Step 1: 并发抓取所有 RSS 源
    all_articles: list[dict] = []
    source_counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=MAX_RSS_WORKERS) as executor:
        futures = {executor.submit(fetch_feed, source, date_str): source for source in sources}
        for future in as_completed(futures):
            src = futures[future]
            try:
                articles = future.result()
                if args.limit:
                    articles = articles[:args.limit]
                all_articles.extend(articles)
                source_counts[src["name"]] = len(articles)
                print(f"[SOURCE] {src['name']}: {len(articles)} 篇", file=sys.stderr)
            except Exception as e:
                src["_fetch_error"] = str(e)
                source_counts[src["name"]] = 0
                print(f"[WARN] {src['name']}: 处理失败: {e}", file=sys.stderr)

    write_source_health(sources, source_counts)

    print(f"[INFO] RSS 抓取完成，共 {len(all_articles)} 篇待处理", file=sys.stderr)

    # Step 2: 并发抓取全文并保存（用 executor.map 保证线程安全）
    def fetch_and_save(article: dict) -> Path:
        idx = _next_idx()
        return save_article(article, out_dir, idx)

    total = 0
    with ThreadPoolExecutor(max_workers=MAX_CONTENT_WORKERS) as executor:
        results = list(executor.map(fetch_and_save, all_articles))
        total = len(results)

    print(f"\n[DONE] 共保存 {total} 篇文章到 {out_dir}", file=sys.stderr)
    print(str(out_dir))  # stdout 输出目录路径，供调用方使用


if __name__ == "__main__":
    main()
