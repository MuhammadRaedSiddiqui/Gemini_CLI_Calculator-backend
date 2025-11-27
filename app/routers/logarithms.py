from fastapi import APIRouter, HTTPException
from app.models.logarithms import LogarithmRequest, LogarithmResponse
from app.services.logarithms import evaluate_logarithmic_function

router = APIRouter()

@router.post("/logarithms/evaluate",
             response_model=LogarithmResponse,
             tags=["Logarithms"],
             summary="Evaluate a logarithmic function",
             description="""
Evaluates a logarithmic function, which can be natural log (ln), base-10 log (log10), or log with a custom base (log).

- **Function Names**: `ln`, `log10`, `log`
- The `base` parameter is **required** when the `function` is `log`.
- The `base` parameter **must not** be provided for `ln` or `log10`.
""")
async def evaluate_log_expression(request: LogarithmRequest):
    """
    Endpoint to evaluate a logarithmic function.

    - **request**: A `LogarithmRequest` model containing:
        - `function`: The `LogarithmicFunction` enum ('ln', 'log10', 'log').
        - `value`: The input float value.
        - `base`: An optional float value for the base (required for 'log').
    """
    try:
        result = evaluate_logarithmic_function(
            function=request.function,
            value=request.value,
            base=request.base
        )
        return LogarithmResponse(
            result=result,
            function=request.function.value,
            input_value=request.value,
            base=request.base
        )
    except ValueError as e:
        # Catches domain errors, invalid base, or missing base from the service/Pydantic model
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
