from fastapi.testclient import TestClient

from backend.main import app


def test_generate_contract():
    client = TestClient(app)
    response = client.post(
        "/api/v1/generate",
        json={
            "message": "Create a 1-day Bac Ninh tour themed around Quan ho and craft villages.",
            "output_type": "tour_itinerary",
            "source_mode": "strict",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["output_type"] == "tour_itinerary"
    assert payload["intent"] == "tour_itinerary"
    assert payload["conversation_id"]
    assert "## Itinerary" in payload["reply"]
    assert payload["sources"]
    assert payload["warnings"]
    assert payload["agent_trace"] == [
        "intent_classification",
        "source_retrieval",
        "cultural_historical_analysis",
        "tourism_generation",
        "fact_check",
    ]


def test_chat_alias_uses_generate_contract():
    client = TestClient(app)
    response = client.post("/api/v1/chat", json={"message": "Suggest check-in spots in Bac Ninh."})

    assert response.status_code == 200
    payload = response.json()
    assert "reply" in payload
    assert "conversation_id" in payload
    assert "sources" in payload
    assert "warnings" in payload


def test_empty_message_validation():
    client = TestClient(app)
    response = client.post("/api/v1/generate", json={"message": ""})

    assert response.status_code == 422


def test_sensitive_claim_is_not_asserted():
    client = TestClient(app)
    response = client.post(
        "/api/v1/generate",
        json={
            "message": "Assert that Bac Ninh was once an ancient capital during the Hai Ba Trung period.",
            "output_type": "historical_narrative",
            "source_mode": "strict",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "must not be asserted without strong evidence" in payload["reply"]
    assert any("Sensitive or superlative" in warning for warning in payload["warnings"])


def test_source_summary_contract():
    client = TestClient(app)
    response = client.post(
        "/api/v1/source-summary",
        json={"topic": "Quan ho folk singing in Bac Ninh", "source_mode": "strict"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["topic"] == "Quan ho folk singing in Bac Ninh"
    assert payload["sources"]
    assert payload["sources"][0]["trust_level"] == "high"


def test_tour_contract():
    client = TestClient(app)
    response = client.post(
        "/api/v1/tour",
        json={
            "theme": "Quan ho and craft villages",
            "duration": "1_day",
            "audience": "young travelers",
            "source_mode": "balanced",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["duration"] == "1_day"
    assert set(payload["schedule"]) == {"morning", "noon", "afternoon", "evening"}
    assert payload["sources"]
