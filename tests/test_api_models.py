import pytest
from credit_limit.api_models import EvaluateApplicationRequest
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
    