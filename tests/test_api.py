from fastapi.testclient import TestClient

from assesswise_shl.api.main import app


def test_health() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_clarifies_when_signal_is_weak() -> None:
    client = TestClient(app)

    response = client.post("/chat", json={"messages": [{"role": "user", "content": "I need help"}]})

    assert response.status_code == 200
    assert set(response.json()) == {"reply", "recommendations", "end_of_conversation"}
    assert response.json()["recommendations"] == []
    assert response.json()["end_of_conversation"] is False
