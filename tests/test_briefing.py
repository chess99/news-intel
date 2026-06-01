from news_intel.briefing import render_daily_brief, render_weekly_review
from news_intel.models import Claim, Event, Evidence, SourceHealth, SourceTier


def test_daily_brief_contains_evidence_and_source_health():
    event = Event(
        id="evt-001",
        date="2026-06-01",
        title="OpenAI introduces Example Model",
        summary="OpenAI introduced an example model.",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=["openai"],
        evidence_ids=["evd-001"],
        claim_links={"claim-agentic-coding": "supports"},
    )
    evidence = {
        "evd-001": Evidence(
            id="evd-001",
            event_id="evt-001",
            source="OpenAI Blog",
            source_tier=SourceTier.T0_FIRST_HAND,
            url="https://openai.com/example",
            quote="OpenAI introduced an example model.",
        )
    }
    health = [
        SourceHealth(
            source="OpenAI Blog",
            tier=SourceTier.T0_FIRST_HAND,
            last_attempt_at="2026-06-01T08:30:00+08:00",
            last_success_at="2026-06-01T08:30:00+08:00",
            status="ok",
            fetched_count=1,
        )
    ]
    text = render_daily_brief("2026-06-01", [event], evidence, health)
    assert "# Personal Tech Radar · 2026-06-01" in text
    assert "Source health" in text
    assert "OpenAI Blog" in text
    assert "Evidence:" in text
    assert "https://openai.com/example" in text


def test_weekly_review_renders_claim_updates():
    claim = Claim(
        id="claim-agentic-coding",
        title="Coding agents are becoming engineering environments",
        status="active",
        confidence="medium",
        summary="Multiple events support the shift from chat assistants to agentic coding environments.",
        supporting_event_ids=["evt-001", "evt-002"],
        updated_at="2026-06-01T09:00:00+08:00",
    )
    text = render_weekly_review("2026-W23", [claim], [])
    assert "# Weekly Tech Radar · 2026-W23" in text
    assert "Coding agents are becoming engineering environments" in text
    assert "active · medium" in text
