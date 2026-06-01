from __future__ import annotations

from news_intel.models import Event, SourceTier


INVESTIGATION_PROMPT = """你是个人科技情报系统的调查 agent。
目标: 对少量高价值事件做证据核验和历史关联，不写日报。

输入包括:
- event JSON
- related evidence JSON
- existing claims JSON

输出严格 JSON:
{
  "event_id": "...",
  "confidence": "low|medium|high",
  "additional_caveats": ["..."],
  "claim_links": {"claim-id": "supports|weakens|contradicts|neutral"},
  "reasoning_summary": "不超过120字，说明证据如何影响判断"
}

规则:
- 优先寻找一手来源。
- 找不到一手来源时，明确说明证据来自二手报道。
- 不根据单一社区讨论建立高置信判断。
- 不创造不存在的历史关联。
"""


def select_events_for_investigation(events: list[Event], *, limit: int = 5) -> list[Event]:
    candidates = [
        event for event in events
        if event.importance >= 4 and SourceTier.T0_FIRST_HAND not in event.source_tiers
    ]
    return sorted(candidates, key=lambda e: (e.importance, e.confidence), reverse=True)[:limit]
