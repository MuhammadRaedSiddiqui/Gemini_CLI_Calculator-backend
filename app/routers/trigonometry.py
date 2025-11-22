from fastapi import APIRouter, HTTPException
from app.models.trigonometry import TrigonometryRequest, TrigonometryResponse, TrigonometricFunction, AngleUnit
from app.services.trigonometry import evaluate_trigonometric_function

router = APIRouter()

@router.post("/trigonometry/evaluate",
             response_model=TrigonometryResponse,
             tags=["Trigonometry"],
             summary="Evaluate a single trigonometric function",
             description="""
Evaluates a standard or hyperbolic trigonometric function for a given value and angle unit.

- **Function Names**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`
- **Angle Units**: `radians`, `degrees`
""")
async def evaluate_trig_expression(request: TrigonometryRequest):
    """
    Endpoint to evaluate a trigonometric function.

    - **request**: A `TrigonometryRequest` model containing:
        - `function`: The `TrigonometricFunction` enum (e.g., "sin").
        - `value`: The input float value.
        - `unit`: The `AngleUnit` enum ("radians" or "degrees").
    """
    try:
        result = evaluate_trigonometric_function(
            function=request.function,
            value=request.value,
            unit=request.unit
        )
        return TrigonometryResponse(
            result=result,
            function=request.function.value,
            input_value=request.value,
            unit=request.unit.value
        )
    except ValueError as e:
        # This catches domain errors or invalid function names from the service
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
