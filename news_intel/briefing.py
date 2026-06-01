from __future__ import annotations

from news_intel.models import Event, Evidence, SourceHealth


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
