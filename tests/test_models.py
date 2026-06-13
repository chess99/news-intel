from news_intel.models import (
    Article,
    Claim,
    DailyEditorial,
    EditorialItem,
    EditorialSource,
    Event,
    Evidence,
    SourceHealth,
    SourceTier,
)


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


def test_daily_editorial_schema_keeps_reader_facing_fields():
    editorial = DailyEditorial(
        date="2026-06-13",
        signal_title="Agent 正在进入团队账本",
        signal_summary="团队开始把 Agent 当成可计量生产资源管理。",
        signal_bullets=["Agent 指标开始从体验叙事转向团队产能账本。"],
        must_read_items=[
            EditorialItem(
                event_id="evt-001",
                headline="Anthropic Fable/Mythos 被监管按下暂停键",
                takeaway="监管边界正在影响前沿模型发布节奏。",
                why_it_matters="这会改变模型公司对安全评估和发布窗口的管理方式。",
                sources=[
                    EditorialSource(
                        name="Anthropic",
                        url="https://anthropic.com/example",
                        tier=SourceTier.T0_FIRST_HAND,
                    )
                ],
                tags=["模型安全", "监管"],
                track_reason="继续跟踪 frontier model 发布边界。",
            )
        ],
    )

    assert editorial.must_read_items[0].sources[0].tier == SourceTier.T0_FIRST_HAND
    assert editorial.scan_items == []
    assert editorial.archive_items == []
