from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .api_models import (
    EvaluateApplicationRequest,
    EvaluateApplicationResponse,
    ValidationErrorResponse
)
from . import evaluate_application, ValidationError

app = FastAPI(title="Credit Limit Core API")

@app.post(
    "/api/v1/applications/evaluate",
    response_model=EvaluateApplicationResponse,
    responses={
        422: {
            "model": ValidationErrorResponse,
        },
    },
)
def evaluate_user_request(body: EvaluateApplicationRequest) -> object:
    response = evaluate_application(
        client_approved_limit=body.client_approved_limit,
        client_outstanding_debt=body.client_outstanding_debt,
        client_reserved_amount=body.client_reserved_amount,
        product_max_limit=body.product_max_limit,
        requested_amount=body.requested_amount,
    )
    if isinstance(response, ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "code": response.code,
                "field": response.field,
            }
        )
    return response
