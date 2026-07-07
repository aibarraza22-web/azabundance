"""Build published Arizona Abundance Index component data."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from pipeline.sources import bps, datacenters

ROOT = Path(__file__).resolve().parents[1]
RAW_BUILD_DIR = ROOT / "data" / "raw" / "build"
TIDY_DIR = ROOT / "data" / "tidy"
PUBLISHED_DIR = ROOT / "data" / "published"
SITE_DATA_DIR = ROOT / "site" / "public" / "data"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _write_csv_json(name: str, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to publish for {name}")
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = PUBLISHED_DIR / f"{name}.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted({key for row in rows for key in row.keys()}))
        writer.writeheader()
        writer.writerows(rows)
    (SITE_DATA_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2) + "\n")


def _quarter(period: str) -> str:
    year, month = period.split("-")
    q = (int(month) - 1) // 3 + 1
    return f"{year}-Q{q}"


def _build_housing_quarterly(monthly_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    totals: dict[tuple[str, str], int] = defaultdict(int)
    meta: dict[tuple[str, str], dict[str, str]] = {}
    for row in monthly_rows:
        key = (_quarter(row["period"]), row["geography"])
        totals[key] += int(row["value"])
        meta[key] = row
    published = []
    for (period, geography), value in sorted(totals.items()):
        source = meta[(period, geography)]
        published.append({
            "metric": "housing_units_permitted",
            "period": period,
            "geography": geography,
            "value": value,
            "unit": "housing units",
            "vintage_date": source["vintage_date"],
            "source_file": source["source_file"],
            "source_url": source["source_url"],
        })
    return published


def _build_manifest(component_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    manifest = []
    for i, row in enumerate(component_rows, start=1):
        manifest.append({
            "figure_id": f"component-{i:03d}",
            "metric": row["metric"],
            "period": row["period"],
            "geography": row["geography"],
            "value": row["value"],
            "source_file": row["source_file"],
        })
    return manifest


def build() -> None:
    bps_raw = bps.fetch(RAW_BUILD_DIR / "bps")
    bps_tidy = bps.parse(bps_raw, TIDY_DIR)
    bps.validate(bps_tidy)

    dc_raw = datacenters.fetch(RAW_BUILD_DIR / "datacenters")
    dc_tidy = datacenters.parse(dc_raw, TIDY_DIR)
    datacenters.validate(dc_tidy)

    housing_monthly = _read_rows(bps_tidy)
    housing_quarterly = _build_housing_quarterly(housing_monthly)
    datacenter_rows = _read_rows(dc_tidy)

    component_rows: list[dict[str, object]] = [*housing_quarterly, *datacenter_rows]
    _write_csv_json("housing_permits_monthly", housing_monthly)
    _write_csv_json("housing_permits_quarterly", housing_quarterly)
    _write_csv_json("datacenter_load", datacenter_rows)
    _write_csv_json("index_components", component_rows)
    _write_csv_json("figure_manifest", _build_manifest(component_rows))


if __name__ == "__main__":
    build()
