from news_intel.briefing import render_daily_brief, render_daily_editorial_brief, render_weekly_review
from news_intel.models import (
    Claim,
    DailyEditorial,
    EditorialItem,
    EditorialSource,
    Event,
    Evidence,
    SourceHealth,
    SourceTier,
)


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
    assert "先看结论" in text
    assert "必读" in text
    assert "信源状态" in text
    assert "OpenAI Blog" in text
    assert "证据：" in text
    assert "https://openai.com/example" in text
    assert "置信度：中" not in text
    assert "event_id" not in text
    assert "claim_id" not in text
    assert "Importance:" not in text
    assert "Evidence:" not in text
    assert "T0_FIRST_HAND" not in text
    assert "claim-agentic-coding" not in text


def test_editorial_brief_renders_signal_newsletter_without_machine_fields():
    editorial = DailyEditorial(
        date="2026-06-13",
        signal_title="Agent 正在进入团队账本",
        signal_summary="这不是又一批 AI 工具发布，而是团队开始把 Agent 当成可计量生产资源管理。",
        signal_bullets=[
            "开发者工具信号比泛融资消息更值得看。",
            "安全和监管事件会直接影响工具采用节奏。",
        ],
        must_read_items=[
            EditorialItem(
                event_id="evt-001",
                headline="Anthropic Fable/Mythos 被监管按下暂停键",
                takeaway="监管边界正在影响前沿模型发布节奏。",
                why_it_matters="这会改变模型公司对安全评估和发布窗口的管理方式。",
                sources=[
                    EditorialSource(
                        name="Anthropic 声明",
                        url="https://anthropic.com/example",
                        tier=SourceTier.T0_FIRST_HAND,
                    ),
                    EditorialSource(
                        name="Wired",
                        url="https://wired.com/example",
                        tier=SourceTier.T1_HIGH_QUALITY_SECONDARY,
                    ),
                ],
                tags=["模型安全", "监管"],
                track_reason="继续跟踪 frontier model 发布边界。",
            )
        ],
        scan_items=[
            EditorialItem(
                event_id="evt-002",
                headline="WebMCP 进入 Chrome Origin Trial",
                takeaway="浏览器侧工具调用能力开始进入实验通道。",
                why_it_matters="",
                sources=[],
                tags=["开发者工具"],
                track_reason="观察真实开发者采用。",
            )
        ],
        archive_items=[
            EditorialItem(
                event_id="evt-003",
                headline="olmo-eval 发布",
                takeaway="模型评测资料，先归档。",
                why_it_matters="",
                sources=[],
                tags=["模型/Agent"],
                track_reason="后续和评测基准变化一起看。",
            )
        ],
    )

    text = render_daily_editorial_brief("2026-06-13", editorial, [])

    assert "> **今日 Signal：Agent 正在进入团队账本**" in text
    assert "## 先看结论" in text
    assert "## 必读" in text
    assert "## 值得扫一眼" in text
    assert "## 资料库" in text
    assert "证据：Anthropic 声明、Wired" in text
    assert "继续跟踪：继续跟踪 frontier model 发布边界。" in text
    assert "evt-001" not in text
    assert "event_id" not in text
    assert "claim_id" not in text
    assert "置信度：中" not in text


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
