from pathlib import Path

from news_intel.fetcher import article_id_from_path, source_slug


def test_source_slug_is_stable():
    assert source_slug("OpenAI Blog") == "openai-blog"
    assert source_slug("36氪") == "36"


def test_article_id_from_path_uses_date_and_stem():
    path = Path("raw/2026/06/01/001-openai-blog-example.md")
    assert article_id_from_path(path) == "2026-06-01-001-openai-blog-example"
