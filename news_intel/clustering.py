from __future__ import annotations

import hashlib

from news_intel.models import Candidate, Event, Evidence, SourceTier


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def normalize_entity_id(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


def cluster_candidates(candidates: list[Candidate]) -> tuple[list[Event], list[Evidence]]:
    groups: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        groups.setdefault(candidate.event_key, []).append(candidate)

    events: list[Event] = []
    evidence_rows: list[Evidence] = []
    for event_key, group in groups.items():
        group = sorted(group, key=lambda c: (c.source_tier.value, c.source, c.id))
        event_id = stable_id("evt", f"{group[0].date}:{event_key}")
        evidence_ids: list[str] = []
        for item in group:
            evidence_id = stable_id("evd", f"{event_id}:{item.id}:{item.url}")
            evidence_rows.append(Evidence(
                id=evidence_id,
                event_id=event_id,
                source=item.source,
                source_tier=item.source_tier,
                url=item.url,
                quote=item.evidence_quote,
            ))
            evidence_ids.append(evidence_id)

        source_tiers = []
        for tier in [
            SourceTier.T0_FIRST_HAND,
            SourceTier.T1_HIGH_QUALITY_SECONDARY,
            SourceTier.T2_COMMUNITY_DISCOVERY,
            SourceTier.T3_CHINESE_SECONDARY,
        ]:
            if any(item.source_tier == tier for item in group):
                source_tiers.append(tier)

        best = max(group, key=lambda c: (c.importance, c.source_tier == SourceTier.T0_FIRST_HAND))
        events.append(Event(
            id=event_id,
            date=best.date,
            title=best.title,
            summary=best.summary,
            importance=max(item.importance for item in group),
            confidence="high" if any(item.source_tier == SourceTier.T0_FIRST_HAND for item in group) else best.confidence,
            source_tiers=source_tiers,
            article_ids=[item.article_id for item in group],
            entity_ids=[normalize_entity_id(e) for item in group for e in item.entities],
            evidence_ids=evidence_ids,
            claim_links={},
        ))
    return events, evidence_rows
