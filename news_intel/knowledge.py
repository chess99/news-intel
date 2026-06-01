from __future__ import annotations

from news_intel.models import Claim, Entity, Event


def update_entities(existing: list[Entity], events: list[Event], *, now: str) -> list[Entity]:
    by_id = {entity.id: entity for entity in existing}
    for event in events:
        for entity_id in event.entity_ids:
            entity = by_id.get(entity_id)
            if entity is None:
                entity = Entity(
                    id=entity_id,
                    name=entity_id.replace("-", " ").title(),
                    kind="topic",
                    event_ids=[],
                    updated_at=now,
                )
            if event.id not in entity.event_ids:
                entity.event_ids.append(event.id)
            entity.updated_at = now
            by_id[entity_id] = entity
    return sorted(by_id.values(), key=lambda e: e.id)


def update_claims(existing: list[Claim], events: list[Event], *, now: str) -> list[Claim]:
    by_id = {claim.id: claim for claim in existing}
    for event in events:
        for claim_id, relation in event.claim_links.items():
            claim = by_id.get(claim_id)
            if claim is None:
                claim = Claim(
                    id=claim_id,
                    title=claim_id.replace("claim-", "").replace("-", " "),
                    status="watching",
                    confidence="low",
                    summary="Created from event linkage.",
                    updated_at=now,
                )
            if relation == "supports" and event.id not in claim.supporting_event_ids:
                claim.supporting_event_ids.append(event.id)
            if relation == "weakens" and event.id not in claim.weakening_event_ids:
                claim.weakening_event_ids.append(event.id)
            if relation == "contradicts" and event.id not in claim.contradicting_event_ids:
                claim.contradicting_event_ids.append(event.id)
            claim.status = derive_claim_status(claim)
            claim.confidence = derive_claim_confidence(claim)
            claim.updated_at = now
            by_id[claim_id] = claim
    return sorted(by_id.values(), key=lambda c: c.id)


def derive_claim_status(claim: Claim) -> str:
    if len(claim.contradicting_event_ids) >= 2:
        return "contradicted"
    if len(claim.weakening_event_ids) > len(claim.supporting_event_ids):
        return "weakened"
    if len(claim.supporting_event_ids) >= 1:
        return "active"
    return claim.status


def derive_claim_confidence(claim: Claim) -> str:
    total = (
        len(claim.supporting_event_ids)
        + len(claim.weakening_event_ids)
        + len(claim.contradicting_event_ids)
    )
    if total >= 5:
        return "high"
    if total >= 2:
        return "medium"
    return "low"
