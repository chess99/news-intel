from __future__ import annotations

from pathlib import Path

from news_intel.fetcher import article_id_from_path
from news_intel.models import Article, SourceTier


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end < 0:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[end + 3 :].strip()


def extract_section(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in markdown:
        return ""
    tail = markdown.split(marker, 1)[1]
    next_heading = tail.find("\n## ")
    if next_heading >= 0:
        tail = tail[:next_heading]
    return tail.strip()


def parse_raw_article(path: Path, *, date: str, source_tiers: dict[str, SourceTier]) -> Article:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    source = meta.get("source", "")
    try:
        article_id = article_id_from_path(path)
    except ValueError:
        article_id = f"{date}-{path.stem}"
    return Article(
        id=article_id,
        date=date,
        source=source,
        source_tier=source_tiers.get(source, SourceTier.T1_HIGH_QUALITY_SECONDARY),
        title=meta.get("title", path.stem),
        url=meta.get("url", ""),
        published=meta.get("published", "")[:10],
        category=meta.get("category", ""),
        raw_path=str(path),
        summary=extract_section(body, "RSS 摘要"),
        body=extract_section(body, "正文") or body,
    )


def should_drop_article(article: Article) -> bool:
    text = f"{article.title}\n{article.summary}\n{article.body}".lower()
    ad_markers = ["限时优惠", "点击领取", "memorial day deals", "best deals", "coupon", "优惠券"]
    if any(marker.lower() in text for marker in ad_markers):
        return True
    if len(article.body.strip()) < 80 and not article.is_first_hand:
        return True
    return False
