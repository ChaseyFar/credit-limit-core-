import pytest
from credit_limit.decision import *


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