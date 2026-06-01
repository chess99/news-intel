from news_intel.knowledge import update_claims, update_entities
from news_intel.models import Claim, Event, SourceTier


def event(id_: str, entity_ids: list[str], claim_links: dict[str, str]) -> Event:
    return Event(
        id=id_,
        date="2026-06-01",
        title="Event",
        summary="Summary",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=entity_ids,
        evidence_ids=["evd-001"],
        claim_links=claim_links,
    )


def test_update_entities_appends_event_ids():
    entities = update_entities([], [event("evt-001", ["openai"], {})], now="2026-06-01T09:00:00+08:00")
    assert entities[0].id == "openai"
    assert entities[0].event_ids == ["evt-001"]


def test_update_claims_tracks_support_and_contradiction():
    existing = [
        Claim(
            id="claim-agentic-coding",
            title="Coding agents are becoming engineering environments",
            status="watching",
            confidence="low",
            summary="Early evidence only.",
            updated_at="2026-05-30T09:00:00+08:00",
        )
    ]
    claims = update_claims(
        existing,
        [event("evt-001", ["openai"], {"claim-agentic-coding": "supports"})],
        now="2026-06-01T09:00:00+08:00",
    )
    assert claims[0].supporting_event_ids == ["evt-001"]
    assert claims[0].status == "active"
