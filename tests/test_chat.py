from fastapi.testclient import TestClient

from backend.main import app


def test_chat_contract(monkeypatch):
    def fake_get_reply(message: str, history: list[dict[str, str]]) -> str:
        return f"Mocked reply for: {message}"

    monkeypatch.setattr("backend.main.get_reply", fake_get_reply)

    client = TestClient(app)
    response = client.post("/api/v1/chat", json={"message": "Plan a trip to Spain"})

    assert response.status_code == 200
    payload = response.json()
    assert "reply" in payload
    assert "conversation_id" in payload
    assert payload["reply"].startswith("Mocked reply for:")
