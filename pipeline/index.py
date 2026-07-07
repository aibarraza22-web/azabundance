"""Build Phase 0 placeholder published artifacts.

Real metric builders must read snapshotted raw data and validated tidy tables.
This module only creates non-observed dummy data for the scaffold site.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_DIR = ROOT / "data" / "published"
SITE_DATA_DIR = ROOT / "site" / "public" / "data"

DUMMY_ROWS = [
    {"period": "2026-Q1", "metric": "Phase 0 placeholder", "value": 100, "status": "DUMMY"},
    {"period": "2026-Q2", "metric": "Phase 0 placeholder", "value": 112, "status": "DUMMY"},
    {"period": "2026-Q3", "metric": "Phase 0 placeholder", "value": 108, "status": "DUMMY"},
    {"period": "2026-Q4", "metric": "Phase 0 placeholder", "value": 121, "status": "DUMMY"},
]


def build() -> None:
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = PUBLISHED_DIR / "placeholder_metric.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DUMMY_ROWS[0].keys())
        writer.writeheader()
        writer.writerows(DUMMY_ROWS)
    (SITE_DATA_DIR / "placeholder_metric.json").write_text(json.dumps(DUMMY_ROWS, indent=2) + "\n")


if __name__ == "__main__":
    build()
