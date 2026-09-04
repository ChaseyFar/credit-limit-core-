from pydantic import BaseModel

class EvaluateApplicationRequest(BaseModel):
    client_approved_limit: int
    client_outstanding_debt: int
    client_reserved_amount: int
    product_max_limit: int
    requested_amount: int

class EvaluateApplicationResponse(BaseModel):
    decision: str
    reason_code: str | None
    allowed_amount: int

class ValidationErrorResponse(BaseModel):
    code: str
    field: str
