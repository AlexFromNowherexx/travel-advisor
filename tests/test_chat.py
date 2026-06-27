from fastapi.testclient import TestClient

from backend.main import app


def test_chat_contract(monkeypatch):
    def fake_get_reply(message: str, history: list[dict[str, str]]) -> str:
        return f"Mocked reply for: {message}"

    monkeypatch.setattr("backend.main.get_reply", fake_get_reply)
    monkeypatch.setattr("backend.main.get_image_results", lambda message: ([], ""))

    client = TestClient(app)
    response = client.post("/api/v1/chat", json={"message": "Plan a trip to Spain"})

    assert response.status_code == 200
    payload = response.json()
    assert "reply" in payload
    assert "conversation_id" in payload
    assert payload["reply"].startswith("Mocked reply for:")
    assert payload["images"] == []
    assert payload["image_html"] == ""


def test_chat_returns_image_html(monkeypatch):
    def fake_get_reply(message: str, history: list[dict[str, str]]) -> str:
        return "Mocked image reply"

    image = {
        "title": "Quan ho Bac Ninh",
        "image_url": "https://example.com/original.jpg",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "source_url": "https://example.com/source",
    }

    monkeypatch.setattr("backend.main.get_reply", fake_get_reply)
    monkeypatch.setattr("backend.main.get_image_results", lambda message: ([image], '<img src="https://example.com/thumb.jpg" alt="Quan ho Bac Ninh" />'))

    client = TestClient(app)
    response = client.post("/api/v1/chat", json={"message": "Search images for Quan ho Bac Ninh"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["images"] == [image]
    assert "<img" in payload["image_html"]
