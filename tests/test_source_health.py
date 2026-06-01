from pathlib import Path

from news_intel.config import load_env_file, load_sources
from news_intel.models import SourceTier
from news_intel.source_health import build_health_record


def test_load_sources_reads_tiers():
    sources = load_sources("sources/feeds.yaml")
    openai = next(s for s in sources if s["name"] == "OpenAI Blog")
    assert openai["tier"] == SourceTier.T0_FIRST_HAND
    assert openai["fetch_strategy"] in {"rss", "html", "browser", "manual"}


def test_build_health_record_for_failed_fetch():
    source = {
        "name": "Anthropic Blog",
        "tier": SourceTier.T0_FIRST_HAND,
    }
    record = build_health_record(
        source=source,
        status="failed",
        fetched_count=0,
        failure_reason="proxy timeout",
        proxy_used="http://127.0.0.1:7890",
        now="2026-06-01T08:30:00+08:00",
        previous={"consecutive_failures": 1, "last_success_at": "2026-05-31T08:30:00+08:00"},
    )
    assert record.consecutive_failures == 2
    assert record.is_stale is True


def test_load_env_file_sets_missing_values(tmp_path: Path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text("EXAMPLE_KEY=example-value\nEXISTING=from-file\n", encoding="utf-8")
    monkeypatch.delenv("EXAMPLE_KEY", raising=False)
    monkeypatch.setenv("EXISTING", "from-env")
    load_env_file(env_path)
    assert __import__("os").environ["EXAMPLE_KEY"] == "example-value"
    assert __import__("os").environ["EXISTING"] == "from-env"
