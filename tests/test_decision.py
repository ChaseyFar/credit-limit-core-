import pytest

from credit_limit.decision import calculate_max_request_amount


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