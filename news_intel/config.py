from __future__ import annotations

from pathlib import Path

import yaml

from news_intel.models import SourceTier


def load_sources(path: str | Path) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sources = []
    for source in data.get("sources", []):
        tier = source.get("tier")
        if not tier:
            raise ValueError(f"source {source.get('name')} missing tier")
        item = dict(source)
        item["tier"] = SourceTier(tier)
        item.setdefault("fetch_strategy", "rss")
        item.setdefault("use_proxy", True)
        sources.append(item)
    return sources
