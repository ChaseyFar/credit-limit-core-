from credit_limit.app import app
from fastapi.testclient import TestClient

def test_credit_limit_app_initialization() -> None:
    assert app.title == "Credit Limit Core API"

def test_open_api() -> None:
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    operation = schema["paths"]["/api/v1/applications/evaluate"]["post"]
    responses = operation["responses"]
    assert "200" in responses
    assert "422" in responses
