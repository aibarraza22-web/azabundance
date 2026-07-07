import csv

from pipeline.index import PUBLISHED_DIR, build


def test_build_writes_placeholder_csv():
    build()
    output = PUBLISHED_DIR / "placeholder_metric.csv"
    assert output.exists()
    rows = list(csv.DictReader(output.open()))
    assert rows
    assert {row["status"] for row in rows} == {"DUMMY"}
