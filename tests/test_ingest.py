from pathlib import Path

from news_intel.fetcher import article_id_from_path, source_slug
from news_intel.ingest import parse_raw_article, should_drop_article
from news_intel.models import SourceTier


def test_source_slug_is_stable():
    assert source_slug("OpenAI Blog") == "openai-blog"
    assert source_slug("36氪") == "36"


def test_article_id_from_path_uses_date_and_stem():
    path = Path("raw/2026/06/01/001-openai-blog-example.md")
    assert article_id_from_path(path) == "2026-06-01-001-openai-blog-example"


def test_parse_raw_article_maps_source_tier():
    source_map = {"OpenAI Blog": SourceTier.T0_FIRST_HAND}
    article = parse_raw_article(
        Path("tests/fixtures/article_official.md"),
        date="2026-06-01",
        source_tiers=source_map,
    )
    assert article.source == "OpenAI Blog"
    assert article.source_tier == SourceTier.T0_FIRST_HAND
    assert "coding capabilities" in article.body


def test_should_drop_article_filters_obvious_ad():
    source_map = {"36氪": SourceTier.T3_CHINESE_SECONDARY}
    article = parse_raw_article(
        Path("tests/fixtures/article_pr.md"),
        date="2026-06-01",
        source_tiers=source_map,
    )
    assert should_drop_article(article) is True
