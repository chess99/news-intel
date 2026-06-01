from __future__ import annotations

from typing import Literal

from news_intel.models import SourceHealth


def build_health_record(
    *,
    source: dict,
    status: Literal["ok", "failed", "empty", "stale"],
    fetched_count: int,
    failure_reason: str,
    proxy_used: str,
    now: str,
    previous: dict | None,
) -> SourceHealth:
    previous = previous or {}
    previous_failures = int(previous.get("consecutive_failures", 0))
    consecutive_failures = 0 if status == "ok" else previous_failures + 1
    last_success_at = now if status == "ok" else previous.get("last_success_at")
    return SourceHealth(
        source=source["name"],
        tier=source["tier"],
        last_attempt_at=now,
        last_success_at=last_success_at,
        status=status,
        consecutive_failures=consecutive_failures,
        fetched_count=fetched_count,
        failure_reason=failure_reason,
        proxy_used=proxy_used,
    )
