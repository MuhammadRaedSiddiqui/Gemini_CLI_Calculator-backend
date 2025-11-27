from fastapi import APIRouter, HTTPException
from app.models.calculus import CalculusRequest, CalculusResponse
from app.services.calculus import perform_calculus_operation

router = APIRouter()

@router.post("/calculus/evaluate",
             response_model=CalculusResponse,
             tags=["Calculus"],
             summary="Perform differentiation or integration on an expression",
             description="""
Performs a symbolic calculus operation on a given expression with respect to the variable 'x'.

- **Operations**: `differentiate`, `integrate`
- For **definite integration**, provide the lower and upper bounds in the `integration_bounds` field (e.g., `[0, 1]`).
- For **indefinite integration** or **differentiation**, omit the `integration_bounds` field.
""")
async def evaluate_calculus_endpoint(request: CalculusRequest):
    """
    Endpoint to perform a calculus operation.

    - **request**: A `CalculusRequest` model.
    """
    try:
        result_str, is_definite = perform_calculus_operation(
            expression_str=request.expression,
            operation=request.operation,
            bounds=request.integration_bounds
        )
        return CalculusResponse(
            result=result_str,
            input_expression=request.expression,
            operation=request.operation.value,
            is_definite_integral=is_definite
        )
    except ValueError as e:
        # Catches errors from the service layer or Pydantic model validation
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # A catch-all for other unexpected server errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
