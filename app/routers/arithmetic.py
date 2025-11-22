from fastapi import APIRouter, HTTPException
from app.models.arithmetic import ArithmeticRequest, ArithmeticResponse
from app.services.arithmetic import evaluate_arithmetic_expression

router = APIRouter()

@router.post("/arithmetic/evaluate",
             response_model=ArithmeticResponse,
             tags=["Arithmetic"],
             summary="Evaluate a basic arithmetic expression",
             description="""
Evaluates a string containing a simple arithmetic expression involving numbers and operators like `+`, `-`, `*`, `/`, `(`, `)`.

**Example:** `(5 + 3) * 2`
""")
async def evaluate_expression(request: ArithmeticRequest):
    """
    Endpoint to evaluate a simple arithmetic expression.
    """
    try:
        result = evaluate_arithmetic_expression(request.expression)
        return ArithmeticResponse(result=result, expression=request.expression)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
