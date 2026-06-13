from news_intel.extraction import extract_candidate
from news_intel.investigation import select_events_for_investigation
from news_intel.models import Article, Event, SourceTier


class ExplodingLLM:
    def complete_json(self, prompt: str) -> dict:
        raise AssertionError("extract should not call per-article LLM")


def test_extract_candidate_is_fast_and_preserves_source_tier_and_url():
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
    candidate = extract_candidate(article, llm=ExplodingLLM())
    assert candidate.article_id == "art-001"
    assert candidate.source_tier == SourceTier.T0_FIRST_HAND
    assert candidate.importance >= 4
    assert candidate.evidence_quote.startswith("OpenAI introduced")


def test_extract_candidate_demotes_funding_and_marketing_news():
    article = Article(
        id="art-002",
        date="2026-06-01",
        source="TechCrunch",
        source_tier=SourceTier.T1_HIGH_QUALITY_SECONDARY,
        title="Startup raises $50M to transform enterprise AI",
        url="https://techcrunch.com/example",
        published="2026-06-01",
        category="business",
        raw_path="raw/2026/06/01/002.md",
        body="A startup raised funding and said it will transform enterprise AI.",
    )

    candidate = extract_candidate(article, llm=ExplodingLLM())

    assert candidate.intent == "deal"
    assert candidate.importance <= 2


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
