from __future__ import annotations

from news_intel.models import Claim, Event, Evidence, SourceHealth


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
        f"> {len(events)} events processed · {len(selected)} selected",
        "",
        "## Source health",
        "",
    ]
    for health in sorted(source_health, key=lambda h: (h.tier.value, h.source)):
        suffix = f" · {health.failure_reason}" if health.failure_reason else ""
        lines.append(f"- {health.source}: {health.status} · {health.fetched_count} items{suffix}")
    lines.extend(["", "## Worth reading", ""])
    for index, event in enumerate(selected, 1):
        lines.append(f"### {index}. {event.title}")
        lines.append("")
        lines.append(f"Importance: {event.importance}/5 · Confidence: {event.confidence}")
        if event.claim_links:
            claim_text = ", ".join(f"{claim_id}={relation}" for claim_id, relation in event.claim_links.items())
            lines.append(f"History: {claim_text}")
        lines.append("")
        lines.append(event.summary)
        lines.append("")
        for evidence_id in event.evidence_ids[:2]:
            evidence = evidence_by_id.get(evidence_id)
            if evidence:
                lines.append(f"- Evidence: {evidence.source} ({evidence.source_tier.value}) - {evidence.url}")
                if evidence.quote:
                    lines.append(f"  Quote: {evidence.quote}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
