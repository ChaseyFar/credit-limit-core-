from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationError:
    code: str
    field: str


def calculate_max_request_amount(
        client_approved_limit: int,
        client_outstanding_debt: int,
        client_reserved_amount: int,
        product_max_limit: int,
        ) -> int:
    available_client_limit = max(0, client_approved_limit-client_outstanding_debt-client_reserved_amount)
    max_request_amount = min(product_max_limit, available_client_limit)
    return max_request_amount

def validate_amount(
        value: object,
        field: str,
        ) -> ValidationError | None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return ValidationError(code="invalid_amount", field=field)
    return None

def validate_positive_amount(
        value: object,
        field: str,
        ) -> ValidationError | None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        return ValidationError(code="invalid_amount", field=field)
    return None

def validate_application_inputs(
        client_approved_limit: object,
        client_outstanding_debt: object,
        client_reserved_amount: object,
        product_max_limit: object,
        requested_amount: object,
        ) -> ValidationError | None:
    raise NotImplementedError