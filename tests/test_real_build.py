import csv

from pipeline.index import PUBLISHED_DIR, build


def test_build_writes_real_component_outputs():
    build()
    components = list(csv.DictReader((PUBLISHED_DIR / "index_components.csv").open()))
    assert components
    assert {row["metric"] for row in components} >= {"housing_units_permitted", "datacenter_load_mw"}
    assert all(row["source_file"] for row in components)
    assert all(row["source_url"] for row in components)
