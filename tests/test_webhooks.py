from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_success_processing():
    response = client.post(
        "/webhooks",
        json={
            "event_id": "test_success",
            "event_type": "payment_success",
            "payload": {}
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "processed"


def test_idempotency():
    payload = {
        "event_id": "duplicate_test",
        "event_type": "payment_success",
        "payload": {}
    }

    client.post("/webhooks", json=payload)

    response = client.post("/webhooks", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Duplicate ignored"


def test_fail_processing():
    response = client.post(
        "/webhooks",
        json={
            "event_id": "fail_test",
            "event_type": "payment_fail",
            "payload": {}
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "failed"


def test_retry_success():

    client.post(
        "/webhooks",
        json={
            "event_id": "retry_test",
            "event_type": "payment_fail",
            "payload": {
                "force_success": True
            }
        }
    )

    response = client.post("/webhooks/retry_test/retry")

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200