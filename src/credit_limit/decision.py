from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationError:
    code: str
    field: str

@dataclass(frozen=True)
class ApplicationDecision:
    decision: str
    reason_code: str | None
    allowed_amount: int


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
    for field_value, field_name in ((requested_amount, "requested_amount"), 
                    (product_max_limit, "product_max_limit")):
        result = validate_positive_amount(value=field_value, field=field_name)
        if result is not None:
            return result
    for field_value, field_name in ((client_approved_limit, "client_approved_limit"), 
                    (client_outstanding_debt, "client_outstanding_debt"), 
                    (client_reserved_amount, "client_reserved_amount")):
        result = validate_amount(value=field_value, field=field_name)
        if result is not None:
            return result
    return None


def evaluate_application(
    client_approved_limit: object,
    client_outstanding_debt: object,
    client_reserved_amount: object,
    product_max_limit: object,
    requested_amount: object,
) -> ValidationError | ApplicationDecision:
    validation_result = validate_application_inputs(client_approved_limit=client_approved_limit,
        client_outstanding_debt=client_outstanding_debt,
        client_reserved_amount=client_reserved_amount,
        product_max_limit=product_max_limit,
        requested_amount=requested_amount
    )
    if validation_result is not None:
        return validation_result
    if requested_amount > product_max_limit:
        return ApplicationDecision(
            decision="rejected",
            reason_code="request_exceeds_product_max_limit",
            allowed_amount=product_max_limit,
        )
    max_request_amount = calculate_max_request_amount(
        client_approved_limit=client_approved_limit,
        client_outstanding_debt=client_outstanding_debt,
        client_reserved_amount=client_reserved_amount,
        product_max_limit=product_max_limit,
    )
    if requested_amount > max_request_amount:
        return ApplicationDecision(
            decision="rejected",
            reason_code="request_exceeds_allowed_amount",
            allowed_amount=max_request_amount,
        )
    return ApplicationDecision(
        decision="approved",
        reason_code=None,
        allowed_amount=max_request_amount,
    )

