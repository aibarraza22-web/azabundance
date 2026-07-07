"""Hand-curated Arizona data center load source."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_SNAPSHOT = ROOT / "data/raw/datacenters/2026-07-07/datacenter_load_curated.csv"


def fetch(raw_dir: Path) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / RAW_SNAPSHOT.name
    shutil.copyfile(RAW_SNAPSHOT, target)
    return target


def parse(raw_path: Path, tidy_dir: Path) -> Path:
    tidy_dir.mkdir(parents=True, exist_ok=True)
    output = tidy_dir / "datacenter_load.csv"
    with raw_path.open(newline="") as src, output.open("w", newline="") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["metric", "period", "geography", "status", "value", "vintage_date", "source_file", "source_url", "method_note"])
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "metric": "datacenter_load_mw",
                "period": row["period"],
                "geography": row["geography"],
                "status": row["status"],
                "value": int(row["value_mw"]),
                "vintage_date": row["retrieved_date"],
                "source_file": str(RAW_SNAPSHOT.relative_to(ROOT)),
                "source_url": row["source_url"],
                "method_note": row["method_note"],
            })
    return output


def validate(tidy_path: Path) -> None:
    with tidy_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Data center tidy output is empty")
    for row in rows:
        if not row["source_url"]:
            raise ValueError(f"Data center row missing source_url: {row}")
        if int(row["value"]) < 0:
            raise ValueError(f"Negative data center MW: {row}")
