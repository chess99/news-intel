from __future__ import annotations

import re
import unicodedata
from pathlib import Path


def source_slug(text: str, max_len: int = 40) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    normalized = re.sub(r"[^\w\s-]", "", normalized.lower())
    normalized = re.sub(r"[\s_-]+", "-", normalized).strip("-")
    return normalized[:max_len] or "untitled"


def article_id_from_path(path: Path) -> str:
    parts = path.parts
    raw_idx = parts.index("raw")
    yyyy, mm, dd = parts[raw_idx + 1 : raw_idx + 4]
    return f"{yyyy}-{mm}-{dd}-{path.stem}"
