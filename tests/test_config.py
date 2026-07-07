from pipeline.config import get_eia_api_key


def test_get_eia_api_key_reads_environment(monkeypatch):
    monkeypatch.setenv("EIA_API_KEY", "demo-key")
    assert get_eia_api_key() == "demo-key"


def test_get_eia_api_key_allows_missing(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    assert get_eia_api_key() is None
