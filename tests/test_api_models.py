import pytest
from pydantic import ValidationError

from credit_limit.api_models import (
    EvaluateApplicationRequest,
    EvaluateApplicationResponse,
    ValidationErrorResponse,
)

<<<<<<< HEAD
def test_evaluate_application_request_model_is_initiated_correctly() -> None:
=======
def test_evaluate_application_request_model_accepts_valid_data() -> None:
>>>>>>> 16d22b1 (style-only v2)
    data = {
        "client_approved_limit": 100_000,
        "client_outstanding_debt": 30_000,
        "client_reserved_amount": 0,
        "product_max_limit": 300_000,
        "requested_amount": 70_000,
    }
    request = EvaluateApplicationRequest(**data)
    assert request.client_approved_limit == 100_000

def test_evaluate_application_request_model_raises_validation_error_on_missing_field() -> None:
    data = {
        "client_approved_limit": 100_000,
        "client_outstanding_debt": 30_000,
        "client_reserved_amount": 0,
        "product_max_limit": 300_000,
    }
    with pytest.raises(ValidationError):
        EvaluateApplicationRequest(**data)

<<<<<<< HEAD
def test_evaluate_application_response_model_is_initiated_correctly() -> None:
=======
def test_evaluate_application_response_model_accepts_valid_data() -> None:
>>>>>>> 16d22b1 (style-only v2)
    data = {
        "decision": "approved",
        "reason_code": None,
        "allowed_amount": 100_000,
    }
    response = EvaluateApplicationResponse(**data)
    assert response.reason_code is None   

def test_evaluate_application_response_model_raises_validation_error_on_missing_field() -> None:
    data = {
        "decision": "approved",
        "reason_code": None,
    }
    with pytest.raises(ValidationError):
        EvaluateApplicationResponse(**data) 

<<<<<<< HEAD
def test_validation_error_model_is_initiated_correctly() -> None:
=======
def test_validation_error_model_accepts_valid_data() -> None:
>>>>>>> 16d22b1 (style-only v2)
    data = {
        "code": "invalid_amount",
        "field": "client_approved_limit",
    }
    response = ValidationErrorResponse(**data)
    assert response.code == "invalid_amount"  

<<<<<<< HEAD
def test_validation_error_model_raises_validation_error_on_missing_field() -> None:
=======
def test_validation_error_model_raises_validation_error_when_code_is_not_a_string() -> None:
>>>>>>> 16d22b1 (style-only v2)
    data = {
        "code": 123,
        "field": "client_approved_limit",
    }
    with pytest.raises(ValidationError):
        ValidationErrorResponse(**data)