from __future__ import annotations

import os
from pathlib import Path


def delivery_payload(date: str, markdown: str) -> dict:
    first_line = next((line for line in markdown.splitlines() if line.startswith("# ")), f"# Personal Tech Radar · {date}")
    return {
        "title": first_line.removeprefix("# ").strip(),
        "body": markdown,
    }


def brief_path(root: Path, date: str) -> Path:
    return root / "brief" / "daily" / f"{date}.md"


def require_feishu_config() -> dict[str, str]:
    required = ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_CHAT_ID"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"missing Feishu configuration: {', '.join(missing)}")
    return {name: os.environ[name] for name in required}
