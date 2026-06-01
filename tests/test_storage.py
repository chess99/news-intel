from pathlib import Path

from news_intel.models import Article, SourceTier
from news_intel.storage import append_jsonl, read_jsonl, write_json


def test_append_and_read_jsonl_round_trip(tmp_path: Path):
    path = tmp_path / "data" / "articles.jsonl"
    article = Article(
        id="art-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Title",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001.md",
    )

    append_jsonl(path, [article.model_dump(mode="json")])

    rows = list(read_jsonl(path))
    assert rows[0]["id"] == "art-001"
    assert rows[0]["source_tier"] == "T0_FIRST_HAND"


def test_write_json_creates_parent_directory(tmp_path: Path):
    path = tmp_path / "state" / "source_health.json"
    write_json(path, {"OpenAI Blog": {"status": "ok"}})
    assert path.exists()
    assert '"OpenAI Blog"' in path.read_text(encoding="utf-8")
