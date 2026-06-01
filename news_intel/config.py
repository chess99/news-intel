from __future__ import annotations

import os
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


def load_env_file(path: str | Path) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
