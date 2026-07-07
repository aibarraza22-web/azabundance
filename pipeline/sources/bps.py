"""BPS housing permits from FRED-hosted Census series snapshots."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_SNAPSHOT = ROOT / "data/raw/fred_bps/2026-07-07/bps_fred_snapshot.csv"
REQUIRED_COLUMNS = {"series_id", "geography", "period", "value", "source_url", "retrieved_date"}


def fetch(raw_dir: Path) -> Path:
    """Snapshot the committed FRED/Census extract into a dated raw directory."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / RAW_SNAPSHOT.name
    shutil.copyfile(RAW_SNAPSHOT, target)
    return target


def parse(raw_path: Path, tidy_dir: Path) -> Path:
    tidy_dir.mkdir(parents=True, exist_ok=True)
    output = tidy_dir / "housing_permits_monthly.csv"
    with raw_path.open(newline="") as src, output.open("w", newline="") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["metric", "period", "geography", "value", "vintage_date", "source_file", "source_url"])
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "metric": "housing_units_permitted",
                "period": row["period"],
                "geography": row["geography"],
                "value": int(row["value"]),
                "vintage_date": row["retrieved_date"],
                "source_file": str(RAW_SNAPSHOT.relative_to(ROOT)),
                "source_url": row["source_url"],
            })
    return output


def validate(tidy_path: Path) -> None:
    with tidy_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("BPS tidy output is empty")
    missing = REQUIRED_COLUMNS - set(csv.DictReader(RAW_SNAPSHOT.open()).fieldnames or [])
    if missing:
        raise ValueError(f"BPS raw snapshot missing columns: {sorted(missing)}")
    for row in rows:
        if int(row["value"]) < 0:
            raise ValueError(f"Negative permit count: {row}")
        if not row["source_url"]:
            raise ValueError(f"Missing source URL: {row}")
