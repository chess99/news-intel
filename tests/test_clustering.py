from news_intel.clustering import cluster_candidates
from news_intel.models import Candidate, SourceTier


def candidate(id_: str, source: str, tier: SourceTier, key: str) -> Candidate:
    return Candidate(
        id=id_,
        article_id=f"art-{id_}",
        date="2026-06-01",
        event_key=key,
        title="OpenAI introduces Example Model",
        summary="OpenAI introduced an example model.",
        source=source,
        source_tier=tier,
        entities=["OpenAI", "Example Model"],
        category="ai_official",
        intent="official_announcement",
        importance=4,
        confidence="high",
        evidence_quote="OpenAI introduced an example model.",
        url=f"https://example.com/{id_}",
    )


def test_cluster_candidates_merges_same_event_key():
    events, evidence = cluster_candidates([
        candidate("001", "OpenAI Blog", SourceTier.T0_FIRST_HAND, "openai-example-model"),
        candidate("002", "The Verge", SourceTier.T1_HIGH_QUALITY_SECONDARY, "openai-example-model"),
    ])
    assert len(events) == 1
    assert len(evidence) == 2
    assert events[0].source_tiers == [SourceTier.T0_FIRST_HAND, SourceTier.T1_HIGH_QUALITY_SECONDARY]
    assert events[0].importance == 4
