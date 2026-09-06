from pydantic import BaseModel
from typing import Literal

ApplicationDecisionType = Literal[
    "approved",
    "rejected",
]

ApplicationRejectReasonCode = Literal[
    "request_exceeds_allowed_amount",
    "request_exceeds_product_max_limit",
]

ApplicationValidationErrorCode = Literal[
    "invalid_amount",
]

ApplicationValidationErrorField = Literal[
    "client_approved_limit",
    "client_outstanding_debt",
    "client_reserved_amount",
    "product_max_limit",
    "requested_amount",
]

class EvaluateApplicationRequest(BaseModel):
    client_approved_limit: int
    client_outstanding_debt: int
    client_reserved_amount: int
    product_max_limit: int
    requested_amount: int

class EvaluateApplicationResponse(BaseModel):
    decision: ApplicationDecisionType
    reason_code: ApplicationRejectReasonCode | None
    allowed_amount: int

class ValidationErrorResponse(BaseModel):
    code: ApplicationValidationErrorCode
    field: ApplicationValidationErrorField
