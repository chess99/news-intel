from __future__ import annotations


def delivery_payload(date: str, markdown: str) -> dict:
    first_line = next((line for line in markdown.splitlines() if line.startswith("# ")), f"# Personal Tech Radar · {date}")
    return {
        "title": first_line.removeprefix("# ").strip(),
        "body": markdown,
    }
