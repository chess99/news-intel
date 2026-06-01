from __future__ import annotations

from news_intel.models import Claim, Event, Evidence, SourceHealth


CONFIDENCE_LABELS = {
    "high": "高",
    "medium": "中",
    "low": "低",
}

SOURCE_STATUS_LABELS = {
    "ok": "正常",
    "failed": "失败",
    "empty": "无新增",
    "stale": "陈旧",
}


def render_daily_brief(
    date: str,
    events: list[Event],
    evidence_by_id: dict[str, Evidence],
    source_health: list[SourceHealth],
) -> str:
    selected = sorted(events, key=lambda e: (e.importance, e.confidence), reverse=True)[:8]
    lines = [
        f"# Personal Tech Radar · {date}",
        "",
        f"今天筛出 {len(selected)} 条值得保留的技术信号。它们不是按热度排序，而是按“是否会改变后续判断”排序。",
        "",
        "## 先看结论",
        "",
    ]
    if selected:
        for event in selected[:3]:
            lines.append(f"- {event.title}：{event.summary}")
    else:
        lines.append("- 今天没有足够明确的高价值信号，建议只检查信源健康和原始抓取结果。")
    lines.extend(["", "## 重点信号", ""])
    for index, event in enumerate(selected, 1):
        lines.append(f"### {index}. {event.title}")
        lines.append("")
        lines.append(event.summary)
        lines.append("")
        lines.append(f"置信度：{CONFIDENCE_LABELS.get(event.confidence, event.confidence)}")
        evidence_lines = render_evidence(event, evidence_by_id)
        if evidence_lines:
            lines.extend(evidence_lines)
        lines.append("")
    lines.extend(render_source_health(source_health))
    return "\n".join(lines).rstrip() + "\n"


def render_evidence(event: Event, evidence_by_id: dict[str, Evidence]) -> list[str]:
    lines = []
    evidence_rows = [evidence_by_id[eid] for eid in event.evidence_ids[:2] if eid in evidence_by_id]
    if not evidence_rows:
        return lines
    for evidence in evidence_rows:
        lines.append(f"依据：{evidence.source}，{evidence.url}")
        if evidence.quote:
            lines.append(f"原文线索：{evidence.quote}")
    return lines


def render_source_health(source_health: list[SourceHealth]) -> list[str]:
    if not source_health:
        return []
    failed = [h for h in source_health if h.status in {"failed", "stale"}]
    empty = [h for h in source_health if h.status == "empty"]
    ok_count = sum(1 for h in source_health if h.status == "ok")
    lines = [
        "## 信源状态",
        "",
        f"本次 {ok_count} 个信源正常抓取，{len(empty)} 个无新增，{len(failed)} 个失败或陈旧。",
    ]
    if failed:
        lines.append("")
        lines.append("需要注意的抓取问题：")
        for health in sorted(failed, key=lambda h: h.source):
            reason = f"：{health.failure_reason}" if health.failure_reason else ""
            status = SOURCE_STATUS_LABELS.get(health.status, health.status)
            lines.append(f"- {health.source}（{status}）{reason}")
    return lines


def render_weekly_review(week_id: str, claims: list[Claim], notable_events: list[Event]) -> str:
    lines = [
        f"# Weekly Tech Radar · {week_id}",
        "",
        "## Claim updates",
        "",
    ]
    for claim in sorted(claims, key=lambda c: (c.status, c.id)):
        evidence_count = (
            len(claim.supporting_event_ids)
            + len(claim.weakening_event_ids)
            + len(claim.contradicting_event_ids)
        )
        if evidence_count == 0:
            continue
        lines.append(f"### {claim.title}")
        lines.append("")
        lines.append(f"Status: {claim.status} · {claim.confidence}")
        lines.append("")
        lines.append(claim.summary)
        lines.append("")
        lines.append(
            f"Supporting: {len(claim.supporting_event_ids)} · "
            f"Weakening: {len(claim.weakening_event_ids)} · "
            f"Contradicting: {len(claim.contradicting_event_ids)}"
        )
        lines.append("")
    lines.append("## Notable events")
    lines.append("")
    for event in sorted(notable_events, key=lambda e: e.importance, reverse=True)[:10]:
        lines.append(f"- {event.title} ({event.importance}/5): {event.summary}")
    return "\n".join(lines).rstrip() + "\n"


def render_monthly_review(month_id: str, claims: list[Claim], notable_events: list[Event]) -> str:
    lines = [
        f"# Monthly Tech Radar · {month_id}",
        "",
        "## What changed",
        "",
    ]
    for claim in sorted(claims, key=lambda c: (c.confidence, c.id), reverse=True):
        if claim.status in {"active", "weakened", "contradicted"}:
            lines.append(f"- {claim.title}: {claim.status} · {claim.confidence}")
    lines.extend(["", "## Events to remember", ""])
    for event in sorted(notable_events, key=lambda e: e.importance, reverse=True)[:15]:
        lines.append(f"- {event.date} · {event.title}")
    return "\n".join(lines).rstrip() + "\n"
