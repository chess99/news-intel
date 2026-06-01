from news_intel.extraction import extract_candidate
from news_intel.models import Article, SourceTier


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
