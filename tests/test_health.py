from fastapi.testclient import TestClient

from backend.main import app


def test_health_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": "0.3.0",
        "service": "bac-bling-agent",
    }
