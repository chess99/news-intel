from news_intel.models import Article, Claim, Event, Evidence, SourceHealth, SourceTier


def test_article_normalizes_source_tier():
    article = Article(
        id="2026-06-01-openai-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Introducing a model",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001-openai.md",
        summary="Official model announcement",
        body="Full body",
    )
    assert article.source_tier == SourceTier.T0_FIRST_HAND
    assert article.is_first_hand is True


def test_source_health_marks_stale_after_failures():
    health = SourceHealth(
        source="Anthropic Blog",
        tier=SourceTier.T0_FIRST_HAND,
        last_attempt_at="2026-06-01T08:30:00+08:00",
        last_success_at="2026-05-29T08:30:00+08:00",
        status="failed",
        consecutive_failures=3,
        fetched_count=0,
        failure_reason="proxy timeout",
        proxy_used="http://127.0.0.1:7890",
    )
    assert health.is_stale is True


def test_event_links_evidence_entities_and_claims():
    evidence = Evidence(
        id="evd-001",
        event_id="evt-001",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        url="https://openai.com/example",
        quote="We are introducing...",
    )
    event = Event(
        id="evt-001",
        date="2026-06-01",
        title="OpenAI introduces a model",
        summary="OpenAI introduced a model.",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=["openai"],
        evidence_ids=[evidence.id],
        claim_links={"claim-agentic-coding": "supports"},
    )
    assert event.claim_links["claim-agentic-coding"] == "supports"
    assert event.confidence == "high"


def test_claim_status_is_conservative():
    claim = Claim(
        id="claim-agentic-coding",
        title="Coding agents are becoming engineering environments",
        status="active",
        confidence="medium",
        summary="Repeated releases indicate a shift from chat to agentic coding environments.",
        supporting_event_ids=["evt-001"],
        weakening_event_ids=[],
        contradicting_event_ids=[],
        updated_at="2026-06-01T09:00:00+08:00",
    )
    assert claim.status == "active"
