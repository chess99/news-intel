from news_intel.editorial import build_editorial
from news_intel.models import Event, Evidence, SourceHealth, SourceTier


def event(
    event_id: str,
    title: str,
    summary: str,
    *,
    importance: int = 3,
    tiers: list[SourceTier] | None = None,
    evidence_ids: list[str] | None = None,
) -> Event:
    return Event(
        id=event_id,
        date="2026-06-13",
        title=title,
        summary=summary,
        importance=importance,
        confidence="medium",
        source_tiers=tiers or [SourceTier.T1_HIGH_QUALITY_SECONDARY],
        article_ids=[f"art-{event_id}"],
        evidence_ids=evidence_ids or [],
    )


def evidence(
    evidence_id: str,
    event_id: str,
    source: str,
    url: str,
    *,
    tier: SourceTier = SourceTier.T1_HIGH_QUALITY_SECONDARY,
) -> Evidence:
    return Evidence(
        id=evidence_id,
        event_id=event_id,
        source=source,
        source_tier=tier,
        url=url,
        quote=f"{source} reported {event_id}.",
    )


def test_editorial_merges_same_story_from_multiple_sources():
    events = [
        event(
            "evt-anthropic-1",
            "Anthropic pauses Fable and Mythos after regulator questions",
            "Anthropic paused the release after safety questions.",
            importance=5,
            tiers=[SourceTier.T0_FIRST_HAND],
            evidence_ids=["evd-a"],
        ),
        event(
            "evt-anthropic-2",
            "Wired says Anthropic Fable/Mythos faces regulator delay",
            "Wired reported a regulator delay for Fable and Mythos.",
            importance=4,
            tiers=[SourceTier.T1_HIGH_QUALITY_SECONDARY],
            evidence_ids=["evd-b"],
        ),
    ]
    evidence_by_id = {
        "evd-a": evidence(
            "evd-a",
            "evt-anthropic-1",
            "Anthropic",
            "https://anthropic.com/news/fable",
            tier=SourceTier.T0_FIRST_HAND,
        ),
        "evd-b": evidence("evd-b", "evt-anthropic-2", "Wired", "https://wired.com/fable"),
    }

    editorial = build_editorial(
        date="2026-06-13",
        events=events,
        evidence_by_id=evidence_by_id,
        source_health=[],
        claims=[],
        llm=None,
    )

    matching = [
        item
        for item in editorial.must_read_items
        if "Anthropic" in item.headline and ("Fable" in item.headline or "Mythos" in item.headline)
    ]
    assert len(matching) == 1
    assert {source.name for source in matching[0].sources} == {"Anthropic", "Wired"}


def test_editorial_prioritizes_security_regulatory_and_developer_tools():
    events = [
        event("evt-funding", "AI startup raises $100M", "A startup raised a large round.", importance=5),
        event(
            "evt-security",
            "PeopleSoft zero-day exploited in the wild",
            "Oracle PeopleSoft has active exploitation reports.",
            importance=4,
        ),
        event(
            "evt-tool",
            "Chrome WebMCP enters Origin Trial",
            "Chrome is testing a developer protocol for browser automation.",
            importance=4,
        ),
    ]

    editorial = build_editorial(
        date="2026-06-13",
        events=events,
        evidence_by_id={},
        source_health=[],
        claims=[],
        llm=None,
    )

    must_read = " ".join(item.headline for item in editorial.must_read_items)
    archive = " ".join(item.headline for item in editorial.archive_items)
    assert "PeopleSoft" in must_read
    assert "WebMCP" in must_read
    assert "raises $100M" in archive


def test_editorial_llm_is_called_once_for_batch_pass():
    class CountingLLM:
        def __init__(self) -> None:
            self.calls = 0

        def complete_json(self, prompt: str) -> dict:
            self.calls += 1
            return {
                "signal_title": "安全和工具链信号同日升温",
                "signal_summary": "今天更值得看的是安全修复和开发者工具能力变化。",
                "signal_bullets": ["安全事件优先级高于泛商业融资。"],
                "must_read_items": [],
                "scan_items": [],
                "archive_items": [],
            }

    llm = CountingLLM()
    events = [
        event(f"evt-{index}", f"Developer tool update {index}", "A useful tool update.", importance=4)
        for index in range(10)
    ]

    editorial = build_editorial(
        date="2026-06-13",
        events=events,
        evidence_by_id={},
        source_health=[],
        claims=[],
        llm=llm,
    )

    assert llm.calls == 1
    assert editorial.signal_title == "安全和工具链信号同日升温"


def test_editorial_includes_source_health_context():
    health = SourceHealth(
        source="Anthropic Blog",
        tier=SourceTier.T0_FIRST_HAND,
        last_attempt_at="2026-06-13T09:00:00+08:00",
        status="failed",
        consecutive_failures=2,
        failure_reason="proxy timeout",
    )

    editorial = build_editorial(
        date="2026-06-13",
        events=[],
        evidence_by_id={},
        source_health=[health],
        claims=[],
        llm=None,
    )

    assert "Anthropic Blog" in editorial.signal_summary
