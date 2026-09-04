import pytest
from credit_limit.api_models import (
    EvaluateApplicationRequest,
    EvaluateApplicationResponse,
    ValidationErrorResponse,
)
from pydantic import ValidationError

def test_evaluate_application_request_model() -> None:
    data = {
        "client_approved_limit": 100_000,
        "client_outstanding_debt": 30_000,
        "client_reserved_amount": 0,
        "product_max_limit": 300_000,
        "requested_amount": 70_000,
    }
    request = EvaluateApplicationRequest(**data)
    assert request.client_approved_limit == 100_000

def test_evaluate_application_request_model_error() -> None:
    data = {
        "client_approved_limit": 100_000,
        "client_outstanding_debt": 30_000,
        "client_reserved_amount": 0,
        "product_max_limit": 300_000,
    }
    with pytest.raises(ValidationError):
        EvaluateApplicationRequest(**data)

def test_evaluate_application_response_model() -> None:
    data = {
        "decision": "approved",
        "reason_code": None,
        "allowed_amount": 100_000,
    }
    response = EvaluateApplicationResponse(**data)
    assert response.reason_code is None   

def test_evaluate_application_response_model_error() -> None:
    data = {
        "decision": "approved",
        "reason_code": None,
    }
    with pytest.raises(ValidationError):
        EvaluateApplicationResponse(**data) 

def test_validation_error_model() -> None:
    data = {
        "code": "invalid_amount",
        "field": "client_approved_limit",
    }
    response = ValidationErrorResponse(**data)
    assert response.code == "invalid_amount"  

def test_validation_error_model_error() -> None:
    data = {
        "code": 123,
        "field": "client_approved_limit",
    }
    with pytest.raises(ValidationError):
        ValidationErrorResponse(**data)