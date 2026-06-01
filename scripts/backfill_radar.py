#!/usr/bin/env python3.11
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date, timedelta


def date_range(start: str, end: str) -> list[str]:
    current = date.fromisoformat(start)
    final = date.fromisoformat(end)
    days = []
    while current <= final:
        days.append(current.isoformat())
        current += timedelta(days=1)
    return days


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args()

    stages = ["ingest", "extract", "cluster", "investigate", "knowledge", "brief"]
    for day in date_range(args.start, args.end):
        for stage in stages:
            subprocess.run(
                [sys.executable, "-m", "news_intel.cli", "stage", stage, "--date", day],
                check=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
