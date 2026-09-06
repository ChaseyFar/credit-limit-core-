from fastapi.testclient import TestClient

from credit_limit.app import app

def test_evaluate_application_approves_correct_user_form() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/applications/evaluate",
        json={
            "client_approved_limit" : 100000,
            "client_outstanding_debt" : 30000,
            "client_reserved_amount" : 0,
            "product_max_limit" : 300000,
            "requested_amount" : 70000,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "decision": "approved",
        "reason_code": None,
        "allowed_amount": 70000,
    }

def test_evaluate_application_returns_422_for_invalid_client_approved_limit() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/applications/evaluate",
        json={
            "client_approved_limit" : -1,
            "client_outstanding_debt" : 30000,
            "client_reserved_amount" : 0,
            "product_max_limit" : 300000,
            "requested_amount" : 70000,
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "code": "invalid_amount",
        "field": "client_approved_limit",
    }
