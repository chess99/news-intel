from news_intel.extraction import extract_candidate
from news_intel.investigation import select_events_for_investigation
from news_intel.models import Article, Event, SourceTier


class FakeLLM:
    def complete_json(self, prompt: str) -> dict:
        return {
            "event_key": "openai-example-model",
            "title": "OpenAI introduces Example Model",
            "summary": "OpenAI introduced an example model with coding capabilities.",
            "entities": ["OpenAI", "Example Model"],
            "intent": "official_announcement",
            "importance": 4,
            "confidence": "high",
            "caveats": ["Performance claims are from official announcement only."],
            "evidence_quote": "OpenAI introduced an example model with new coding capabilities.",
        }


def test_extract_candidate_preserves_source_tier_and_url():
    article = Article(
        id="art-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Introducing Example Model",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001.md",
        body="OpenAI introduced an example model with new coding capabilities.",
    )
    candidate = extract_candidate(article, llm=FakeLLM())
    assert candidate.article_id == "art-001"
    assert candidate.source_tier == SourceTier.T0_FIRST_HAND
    assert candidate.importance == 4
    assert candidate.evidence_quote.startswith("OpenAI introduced")


def test_select_events_for_investigation_prioritizes_important_and_non_first_hand():
    events = [
        Event(
            id="evt-low",
            date="2026-06-01",
            title="Low",
            summary="Low",
            importance=2,
            confidence="medium",
            source_tiers=[SourceTier.T1_HIGH_QUALITY_SECONDARY],
            article_ids=["art-1"],
        ),
        Event(
            id="evt-important-secondary",
            date="2026-06-01",
            title="Important",
            summary="Important",
            importance=5,
            confidence="medium",
            source_tiers=[SourceTier.T1_HIGH_QUALITY_SECONDARY],
            article_ids=["art-2"],
        ),
    ]
    selected = select_events_for_investigation(events, limit=3)
    assert [event.id for event in selected] == ["evt-important-secondary"]
