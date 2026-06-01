from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class SourceTier(str, Enum):
    T0_FIRST_HAND = "T0_FIRST_HAND"
    T1_HIGH_QUALITY_SECONDARY = "T1_HIGH_QUALITY_SECONDARY"
    T2_COMMUNITY_DISCOVERY = "T2_COMMUNITY_DISCOVERY"
    T3_CHINESE_SECONDARY = "T3_CHINESE_SECONDARY"


class Article(BaseModel):
    id: str
    date: str
    source: str
    source_tier: SourceTier
    title: str
    url: str
    published: str
    category: str
    raw_path: str
    summary: str = ""
    body: str = ""

    @property
    def is_first_hand(self) -> bool:
        return self.source_tier == SourceTier.T0_FIRST_HAND


class SourceHealth(BaseModel):
    source: str
    tier: SourceTier
    last_attempt_at: str
    last_success_at: str | None = None
    status: Literal["ok", "failed", "empty", "stale"]
    consecutive_failures: int = 0
    fetched_count: int = 0
    failure_reason: str = ""
    proxy_used: str = ""

    @property
    def is_stale(self) -> bool:
        return self.status in {"failed", "stale"} and self.consecutive_failures >= 2


class Candidate(BaseModel):
    id: str
    article_id: str
    date: str
    event_key: str
    title: str
    summary: str
    source: str
    source_tier: SourceTier
    entities: list[str] = Field(default_factory=list)
    category: str
    intent: Literal[
        "official_announcement",
        "reporting",
        "commentary",
        "pr",
        "community_discussion",
        "deal",
        "tutorial",
        "research",
        "regulatory",
    ]
    importance: int = Field(ge=1, le=5)
    confidence: Literal["low", "medium", "high"]
    caveats: list[str] = Field(default_factory=list)
    evidence_quote: str = ""
    url: str


class Evidence(BaseModel):
    id: str
    event_id: str
    source: str
    source_tier: SourceTier
    url: str
    quote: str


class Event(BaseModel):
    id: str
    date: str
    title: str
    summary: str
    importance: int = Field(ge=1, le=5)
    confidence: Literal["low", "medium", "high"]
    source_tiers: list[SourceTier]
    article_ids: list[str]
    entity_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    claim_links: dict[
        str,
        Literal["supports", "weakens", "contradicts", "neutral"],
    ] = Field(default_factory=dict)


class Entity(BaseModel):
    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    kind: Literal["company", "product", "person", "technology", "regulator", "project", "topic"]
    event_ids: list[str] = Field(default_factory=list)
    updated_at: str


class Claim(BaseModel):
    id: str
    title: str
    status: Literal["active", "watching", "weakened", "contradicted", "retired"]
    confidence: Literal["low", "medium", "high"]
    summary: str
    supporting_event_ids: list[str] = Field(default_factory=list)
    weakening_event_ids: list[str] = Field(default_factory=list)
    contradicting_event_ids: list[str] = Field(default_factory=list)
    updated_at: str
