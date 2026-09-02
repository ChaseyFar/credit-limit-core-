import pytest
from pytest import MonkeyPatch
from credit_limit.decision import *
from credit_limit import decision

@pytest.mark.parametrize(
    (
        "client_approved_limit, "
        "client_outstanding_debt, "
        "client_reserved_amount, "
        "product_max_limit, "
        "expected_amount"
    ),
    [
        (10_000_000, 7_000_000, 4_000_000, 30_000_000, 0),
        (100_000_000, 50_000_000, 10_000_000, 30_000_000, 30_000_000),
        (100_000_000, 50_000_000, 30_000_000, 30_000_000, 20_000_000),
        (100_000_000, 40_000_000, 30_000_000, 30_000_000, 30_000_000),
        (10_000_000, 7_000_000, 3_000_000, 30_000_000, 0)
    ],
)
def test_calculate_max_request_amount(
    client_approved_limit: int,
    client_outstanding_debt: int,
    client_reserved_amount: int,
    product_max_limit: int,
    expected_amount: int,
) -> None:
    actual_amount = calculate_max_request_amount(
        client_approved_limit=client_approved_limit,
        client_outstanding_debt=client_outstanding_debt,
        client_reserved_amount=client_reserved_amount,
        product_max_limit=product_max_limit,
    )

    assert actual_amount == expected_amount


@pytest.mark.parametrize("value", [1.5, -1, True])
def test_validate_amount_negative(
    value: object
) -> None:
    field = "client_approved_limit"
    result = validate_amount(value=value, field=field)

    assert result == ValidationError(
        code="invalid_amount",
        field=field,
    )

@pytest.mark.parametrize("value", [0, 100_000])
def test_validate_amount_positive(
    value: object
) -> None:
    field = "client_approved_limit"
    result = validate_amount(value=value, field=field)

    assert result is None

@pytest.mark.parametrize("value", [0, -1, 1.5, True])
def test_validate_positive_amount_negative(
    value: object,
) -> None:
    field = "product_max_limit"
    result = validate_positive_amount(value=value, field=field)
    
    assert result == ValidationError(
        code="invalid_amount",
        field=field,
    )

@pytest.mark.parametrize("value", [1, 100_000])
def test_validate_positive_amount_positive(
    value: object,
) -> None:
    field = "product_max_limit"
    result = validate_positive_amount(value=value, field=field)
    
    assert result is None

@pytest.mark.parametrize("field", ["client_approved_limit", "client_outstanding_debt","client_reserved_amount"])
def test_validate_amount_and_field_positive(
    field: str
) -> None:
    result = validate_amount(value=0, field=field)
    
    assert result is None

def test_validate_application_inputs_order() -> None:
    result = validate_application_inputs(client_approved_limit=1,
            client_outstanding_debt=1,
            client_reserved_amount = 1,
            product_max_limit = 0,
            requested_amount = 0
            )
    
    assert result == ValidationError(code="invalid_amount", field="requested_amount")

@pytest.mark.parametrize(
    (
        "client_approved_limit",
        "client_outstanding_debt",
        "client_reserved_amount",
        "product_max_limit",
        "requested_amount"
    ),
    [
        (0, 0, 0, 1, 1),
        (1, 1, 1, 1, 1)
    ]
)
def test_validate_application_inputs_positive(
    client_approved_limit: object,
    client_outstanding_debt: object,
    client_reserved_amount: object,
    product_max_limit: object,
    requested_amount: object,
) -> None:
    result = validate_application_inputs(client_approved_limit=client_approved_limit,
                client_outstanding_debt=client_outstanding_debt,
                client_reserved_amount=client_reserved_amount,
                product_max_limit=product_max_limit,
                requested_amount=requested_amount
                )

    assert result is None

@pytest.mark.parametrize(
    (
        "client_approved_limit",
        "client_outstanding_debt",
        "client_reserved_amount",
        "product_max_limit",
        "requested_amount",
        "expected_allowed_amount"
    ),
    [
        (100_000_000, 40_000_000, 30_000_000, 30_000_000, 10_000_000, 30_000_000),
        (100_000_000, 40_000_000, 30_000_000, 30_000_000, 30_000_000, 30_000_000)
    ]
)
def test_evaluate_application_approve(
    client_approved_limit: object,
    client_outstanding_debt: object,
    client_reserved_amount: object,
    product_max_limit: object,
    requested_amount: object,
    expected_allowed_amount: object
) -> None:
    result = evaluate_application(client_approved_limit=client_approved_limit,
                client_outstanding_debt=client_outstanding_debt,
                client_reserved_amount=client_reserved_amount,
                product_max_limit=product_max_limit,
                requested_amount=requested_amount
                )
    assert result == ApplicationDecision(decision="approved", reason_code=None, allowed_amount=expected_allowed_amount)


def test_evaluate_application_rejects_request_above_allowed_amount() -> None:
    result = evaluate_application(client_approved_limit=100_000,
        client_outstanding_debt=30_000,
        client_reserved_amount=0,
        product_max_limit=80_000,
        requested_amount=70_001
        )
    assert result == ApplicationDecision(
        decision="rejected",  
        reason_code='request_exceeds_allowed_amount', 
        allowed_amount=70_000)

def test_evaluate_application_rejects_request_above_product_max_limit() -> None:
    result = evaluate_application(
        client_approved_limit=500_000,
        client_outstanding_debt=0,
        client_reserved_amount=0,
        product_max_limit=100_000,
        requested_amount=400_000,
    )
    assert result == ApplicationDecision(
        decision="rejected",
        reason_code="request_exceeds_product_max_limit",
        allowed_amount=100_000,
    )

@pytest.mark.parametrize(
    (
        "client_approved_limit",
        "client_outstanding_debt",
        "client_reserved_amount",
        "product_max_limit",
        "requested_amount",
        "expected_field"
    ),
    [
        (-1, -1, -1, 0, 0, "requested_amount"),
        (-1, -1, -1, 0, 1, "product_max_limit"),
        (-1, -1, -1, 1, 1, "client_approved_limit"),
        (0, -1, -1, 1, 1, "client_outstanding_debt"),
        (0, 0, -1, 1, 1, "client_reserved_amount"),
        (1, 1, 1, 1, None, "requested_amount"),
        (0, 0, False, 1, 1, "client_reserved_amount"),
        (1, 1, 1, "1", 1, "product_max_limit"),
        ("1", 1, 1, 1, 1, "client_approved_limit"),
        (1, 1.5, 1, 1, 1, "client_outstanding_debt")
    ]
)
def test_evaluate_application_returns_validation_error(
    client_approved_limit: object,
    client_outstanding_debt: object,
    client_reserved_amount: object,
    product_max_limit: object,
    requested_amount: object,
    expected_field: str
) -> None:
    result = evaluate_application(client_approved_limit=client_approved_limit,
        client_outstanding_debt=client_outstanding_debt,
        client_reserved_amount=client_reserved_amount,
        product_max_limit=product_max_limit,
        requested_amount=requested_amount
    )

def test_evaluate_application_executes_no_calculation_after_exceeding_product_limit(
    monkeypatch: MonkeyPatch
) -> None:
    def must_not_be_called(**_: object) -> int:
        raise AssertionError("Calculation must not be called")
    monkeypatch.setattr(decision, "calculate_max_request_amount", must_not_be_called)
    result = evaluate_application(
        client_approved_limit=500_000,
        client_outstanding_debt=0,
        client_reserved_amount=0,
        product_max_limit=100_000,
        requested_amount=400_000,
    )
    assert result == ApplicationDecision(
        decision="rejected",
        reason_code="request_exceeds_product_max_limit",
        allowed_amount=100_000,
    )

@pytest.mark.parametrize(
    (
        "client_approved_limit",
        "client_outstanding_debt",
        "client_reserved_amount",
        "product_max_limit",
        "requested_amount",
        "expected_result"
    ),
    [
        (100_000, 30_000, 0, 80_000, 60_000, 
            ApplicationDecision(decision="approved", reason_code=None, allowed_amount=70_000,)),
        (100_000, 30_000, 0, 80_000, 70_000, 
            ApplicationDecision(decision="approved", reason_code=None, allowed_amount=70_000,)),
        (100_000, 30_000, 0, 80_000, 70_001, 
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_allowed_amount", allowed_amount=70_000,)),
        (500_000, 0, 0, 100_000, 400_000, 
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_product_max_limit", allowed_amount=100_000,)),
        (100_000, 80_000, 0, 50_000, 60_000, 
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_product_max_limit", allowed_amount=50_000,)),
        (100_000, 40_000, 10_000, 80_000, 50_000, 
            ApplicationDecision(decision="approved", reason_code=None, allowed_amount=50_000,)),
        (100_000, 70_000, 30_000, 100_000, 1, 
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_allowed_amount", allowed_amount=0,)),
        (100_000, 70_001, 30_000, 100_000, 1,
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_allowed_amount", allowed_amount=0,)),
        (0, 0, 0, 10_000, 1, 
            ApplicationDecision(decision="rejected", reason_code="request_exceeds_allowed_amount", allowed_amount=0,))
    ]
)
def test_evaluate_application_full_scenario(
    client_approved_limit: object,
    client_outstanding_debt: object,
    client_reserved_amount: object,
    product_max_limit: object,
    requested_amount: object,
    expected_result: object
) -> None:
    result = evaluate_application(client_approved_limit=client_approved_limit,
        client_outstanding_debt=client_outstanding_debt,
        client_reserved_amount=client_reserved_amount,
        product_max_limit=product_max_limit,
        requested_amount=requested_amount
    )
    assert result == expected_result