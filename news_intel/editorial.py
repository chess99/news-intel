from __future__ import annotations

import json
import re
from collections import defaultdict

from pydantic import ValidationError

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


EDITORIAL_PROMPT = """你是 Personal Tech Radar 的主编。
只输出 JSON 对象，不输出 Markdown。

目标:
- 先给今日 Signal 判断，再给证据。
- 合并同一事件的重复来源。
- 优先排序: 一手源、监管/安全/开发者工具/模型能力变化。
- 降权: 融资、营销、泛商业叙事。
- 每个 item 最多保留 3 个来源。
- 不输出 event_id、claim_id 等机器字段给读者，但 JSON item 内需要保留 event_id 供系统追踪。

JSON schema:
{
  "signal_title": "...",
  "signal_summary": "...",
  "signal_bullets": ["...", "..."],
  "must_read_items": [
    {
      "event_id": "...",
      "headline": "...",
      "takeaway": "...",
      "why_it_matters": "...",
      "sources": [{"name": "...", "url": "...", "tier": "T0_FIRST_HAND", "quote": "..."}],
      "tags": ["..."],
      "track_reason": "..."
    }
  ],
  "scan_items": [],
  "archive_items": []
}

输入:
{payload}
"""

SECURITY_TERMS = {
    "zero-day",
    "0-day",
    "cve",
    "exploit",
    "exploited",
    "malicious",
    "rce",
    "vulnerability",
    "breach",
    "恶意",
    "漏洞",
    "供应链攻击",
}
REGULATORY_TERMS = {"regulator", "regulatory", "safety", "paused", "pause", "监管", "暂停", "合规"}
TOOL_TERMS = {"developer", "tool", "tools", "sdk", "api", "cli", "chrome", "webmcp", "github", "colab"}
MODEL_TERMS = {"model", "agent", "agents", "llm", "eval", "benchmark", "inference"}
DEAL_TERMS = {"raises", "raised", "funding", "financing", "series", "ipo", "valuation", "$", "融资"}


def build_editorial(
    *,
    date: str,
    events: list[Event],
    evidence_by_id: dict[str, Evidence],
    source_health: list[SourceHealth],
    claims: list[Claim],
    llm: object | None,
) -> DailyEditorial:
    groups = merge_related_events(events)
    fallback = deterministic_editorial(
        date=date,
        groups=groups,
        evidence_by_id=evidence_by_id,
        source_health=source_health,
    )
    if llm is None:
        return fallback

    try:
        payload = editorial_payload(groups, evidence_by_id, source_health, claims)
        prompt = EDITORIAL_PROMPT.replace("{payload}", json.dumps(payload, ensure_ascii=False))
        data = llm.complete_json(prompt)
        data.setdefault("date", date)
        return DailyEditorial.model_validate(data)
    except (KeyError, TypeError, ValueError, ValidationError, AttributeError):
        return fallback


def merge_related_events(events: list[Event]) -> list[list[Event]]:
    grouped: dict[str, list[Event]] = defaultdict(list)
    for item in events:
        grouped[topic_key(item)].append(item)
    return list(grouped.values())


def topic_key(event: Event) -> str:
    lower = f"{event.title} {event.summary}".lower()
    if "anthropic" in lower and ("fable" in lower or "mythos" in lower):
        return "anthropic-fable-mythos-regulatory-pause"
    if "peoplesoft" in lower and ("zero-day" in lower or "0-day" in lower or "exploit" in lower):
        return "oracle-peoplesoft-zero-day-exploitation"
    if "webmcp" in lower and "chrome" in lower:
        return "chrome-webmcp-origin-trial"

    tokens = re.findall(r"[a-zA-Z0-9]+", lower)
    meaningful = [
        token
        for token in tokens
        if len(token) > 2
        and token
        not in {
            "the",
            "and",
            "for",
            "with",
            "from",
            "after",
            "says",
            "new",
            "launches",
            "introduces",
        }
    ]
    return "-".join(meaningful[:6]) or event.id


def deterministic_editorial(
    *,
    date: str,
    groups: list[list[Event]],
    evidence_by_id: dict[str, Evidence],
    source_health: list[SourceHealth],
) -> DailyEditorial:
    ranked = sorted(groups, key=lambda group: group_score(group), reverse=True)
    must_read: list[EditorialItem] = []
    scan: list[EditorialItem] = []
    archive: list[EditorialItem] = []

    for group in ranked:
        item = editorial_item(group, evidence_by_id)
        score = group_score(group)
        if score >= 6 and len(must_read) < 5:
            must_read.append(item)
        elif score >= 4 and len(scan) < 6:
            scan.append(item)
        else:
            archive.append(item)

    if not must_read and scan:
        must_read.append(scan.pop(0))

    bullets = signal_bullets(must_read, scan, source_health)
    return DailyEditorial(
        date=date,
        signal_title=signal_title(must_read, scan, source_health),
        signal_summary=signal_summary(must_read, scan, source_health),
        signal_bullets=bullets[:3],
        must_read_items=must_read,
        scan_items=scan,
        archive_items=archive[:8],
    )


def editorial_item(group: list[Event], evidence_by_id: dict[str, Evidence]) -> EditorialItem:
    best = max(group, key=lambda event: (event.importance, has_first_hand(event)))
    sources = sources_for_group(group, evidence_by_id)
    tags = tags_for_text(" ".join(f"{event.title} {event.summary}" for event in group))
    return EditorialItem(
        event_id=best.id,
        headline=best.title,
        takeaway=best.summary,
        why_it_matters=why_it_matters(best, tags),
        sources=sources,
        tags=tags,
        track_reason=track_reason(tags),
    )


def sources_for_group(group: list[Event], evidence_by_id: dict[str, Evidence]) -> list[EditorialSource]:
    seen: set[tuple[str, str]] = set()
    sources: list[EditorialSource] = []
    evidence_rows: list[Evidence] = []
    for event in group:
        evidence_rows.extend(evidence_by_id[eid] for eid in event.evidence_ids if eid in evidence_by_id)
    evidence_rows = sorted(evidence_rows, key=lambda row: tier_rank(row.source_tier))
    for row in evidence_rows:
        key = (row.source, row.url)
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            EditorialSource(
                name=row.source,
                url=row.url,
                tier=row.source_tier,
                quote=row.quote,
            )
        )
        if len(sources) >= 3:
            break
    return sources


def group_score(group: list[Event]) -> int:
    text = " ".join(f"{event.title} {event.summary}" for event in group).lower()
    score = max(event.importance for event in group)
    if any(has_first_hand(event) for event in group):
        score += 1
    if has_any(text, SECURITY_TERMS):
        score += 5
    if has_any(text, REGULATORY_TERMS):
        score += 5
    if has_any(text, TOOL_TERMS):
        score += 2
    if has_any(text, MODEL_TERMS):
        score += 1
    if has_any(text, DEAL_TERMS):
        score -= 5
    if max(len(event.summary) for event in group) < 24:
        score -= 3
    return score


def tags_for_text(text: str) -> list[str]:
    lower = text.lower()
    tags: list[str] = []
    if has_any(lower, SECURITY_TERMS):
        tags.append("安全/风险")
    if has_any(lower, REGULATORY_TERMS):
        tags.append("监管/安全边界")
    if has_any(lower, TOOL_TERMS):
        tags.append("开发者工具")
    if has_any(lower, MODEL_TERMS):
        tags.append("模型/Agent")
    if has_any(lower, DEAL_TERMS):
        tags.append("商业动态")
    return tags or ["技术信号"]


def why_it_matters(event: Event, tags: list[str]) -> str:
    if "安全/风险" in tags:
        return "安全事件会直接改变升级、排查和供应链防护优先级。"
    if "监管/安全边界" in tags:
        return "监管和安全边界会影响模型或产品的发布节奏，也会改变后续采用判断。"
    if "开发者工具" in tags:
        return "开发者工具的能力变化会进入日常工作流，值得比营销发布更早观察。"
    if "模型/Agent" in tags:
        return "模型能力和评测变化会影响后续工具选择与长期假设。"
    if "商业动态" in tags:
        return "商业动作本身信息密度有限，除非后续出现产品或技术证据。"
    return event.summary


def track_reason(tags: list[str]) -> str:
    if "安全/风险" in tags:
        return "影响范围、补丁状态、真实利用情况。"
    if "监管/安全边界" in tags:
        return "监管口径、发布边界、模型安全评估。"
    if "开发者工具" in tags:
        return "真实开发者采用、API 稳定性、生态集成。"
    if "模型/Agent" in tags:
        return "评测复现、能力边界、成本变化。"
    return "后续是否出现一手证据或可验证进展。"


def signal_title(
    must_read: list[EditorialItem],
    scan: list[EditorialItem],
    source_health: list[SourceHealth],
) -> str:
    items = must_read + scan
    tag_text = " ".join(tag for item in items for tag in item.tags)
    if "安全/风险" in tag_text and "监管/安全边界" in tag_text:
        return "安全与监管正在同时改变技术采用节奏"
    if "开发者工具" in tag_text and "模型/Agent" in tag_text:
        return "Agent 能力正在落进开发者工作流"
    if any(health.is_stale for health in source_health):
        return "一手信源健康需要先校准"
    if items:
        return f"{items[0].headline} 是今天最值得跟的信号"
    return "今天没有足够明确的高价值信号"


def signal_summary(
    must_read: list[EditorialItem],
    scan: list[EditorialItem],
    source_health: list[SourceHealth],
) -> str:
    stale = [health.source for health in source_health if health.is_stale]
    if stale and not must_read and not scan:
        return f"今天事件密度不高，但 {', '.join(stale[:3])} 抓取异常，需要先看信源健康。"
    if must_read:
        return "今天值得先看的不是热度最高的消息，而是会改变安全边界、工具采用或模型判断的信号。"
    if scan:
        return "今天没有强主线，但有几条值得轻扫并归档的技术变化。"
    return "今天没有足够明确的高价值信号，保留信源状态供排查。"


def signal_bullets(
    must_read: list[EditorialItem],
    scan: list[EditorialItem],
    source_health: list[SourceHealth],
) -> list[str]:
    items = must_read + scan
    bullets = []
    if items:
        bullets.append(f"先读 {items[0].headline}，它最可能改变后续判断。")
    if any("安全/风险" in item.tags for item in items):
        bullets.append("安全事件优先看影响范围、补丁状态和真实利用证据。")
    if any("开发者工具" in item.tags for item in items):
        bullets.append("开发者工具变化只在进入实际工作流时才值得长期跟踪。")
    stale = [health.source for health in source_health if health.is_stale]
    if stale:
        bullets.append(f"{', '.join(stale[:2])} 抓取异常，今天的一手源覆盖不完整。")
    return bullets or ["今天没有足够明确的高价值信号，建议只保留归档。"]


def editorial_payload(
    groups: list[list[Event]],
    evidence_by_id: dict[str, Evidence],
    source_health: list[SourceHealth],
    claims: list[Claim],
) -> dict:
    ranked = sorted(groups, key=lambda group: group_score(group), reverse=True)[:20]
    return {
        "events": [
            {
                "ids": [event.id for event in group],
                "title": editorial_item(group, evidence_by_id).headline,
                "summary": editorial_item(group, evidence_by_id).takeaway,
                "importance": max(event.importance for event in group),
                "tags": tags_for_text(" ".join(f"{event.title} {event.summary}" for event in group)),
                "sources": [source.model_dump(mode="json") for source in sources_for_group(group, evidence_by_id)],
            }
            for group in ranked
        ],
        "source_health": [
            {
                "source": health.source,
                "status": health.status,
                "consecutive_failures": health.consecutive_failures,
                "failure_reason": health.failure_reason,
            }
            for health in source_health
            if health.status != "ok"
        ],
        "claims": [
            {
                "id": claim.id,
                "title": claim.title,
                "status": claim.status,
                "summary": claim.summary,
            }
            for claim in claims[:20]
        ],
    }


def has_first_hand(event: Event) -> bool:
    return SourceTier.T0_FIRST_HAND in event.source_tiers


def tier_rank(tier: SourceTier) -> int:
    order = {
        SourceTier.T0_FIRST_HAND: 0,
        SourceTier.T1_HIGH_QUALITY_SECONDARY: 1,
        SourceTier.T2_COMMUNITY_DISCOVERY: 2,
        SourceTier.T3_CHINESE_SECONDARY: 3,
    }
    return order[tier]


def has_any(text: str, terms: set[str]) -> bool:
    for term in terms:
        if needs_word_boundary(term):
            if re.search(rf"(?<![a-zA-Z0-9]){re.escape(term)}(?![a-zA-Z0-9])", text):
                return True
        elif term in text:
            return True
    return False


def needs_word_boundary(term: str) -> bool:
    return all(ord(char) < 128 for char in term) and any(char.isalnum() for char in term)
