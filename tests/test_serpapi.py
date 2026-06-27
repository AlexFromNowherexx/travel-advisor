import pytest
from backend.serpapi_client import SerpApiClient


def test_serpapi_disabled_by_default(monkeypatch):
    monkeypatch.setattr("backend.serpapi_client.settings.serpapi_api_key", None)
    client = SerpApiClient()
    assert not client.enabled()
    assert client.search("test") == []


def test_serpapi_enabled_if_key_set(monkeypatch):
    monkeypatch.setattr("backend.serpapi_client.settings.serpapi_api_key", "fake_key")
    client = SerpApiClient()
    assert client.enabled()
