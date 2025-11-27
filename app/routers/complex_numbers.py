from fastapi import APIRouter, HTTPException
from app.models.complex_numbers import ComplexArithmeticRequest, ComplexArithmeticResponse
from app.services.complex_numbers import evaluate_complex_arithmetic

router = APIRouter()

@router.post("/complex/evaluate",
             response_model=ComplexArithmeticResponse,
             tags=["Complex Numbers"],
             summary="Perform arithmetic on two complex numbers",
             description="""
Performs addition, subtraction, multiplication, or division on two complex numbers.

- **Complex Number Format**: Numbers must be provided as strings in the format `a+bj` or `a-bj`.
- **Operations**: `add`, `subtract`, `multiply`, `divide`.
""")
async def evaluate_complex_endpoint(request: ComplexArithmeticRequest):
    """
    Endpoint to perform arithmetic on complex numbers.

    - **request**: A `ComplexArithmeticRequest` model containing:
        - `num1`: The first complex number string.
        - `num2`: The second complex number string.
        - `operation`: The operation to perform.
    """
    try:
        result, calc_str = evaluate_complex_arithmetic(
            num1_str=request.num1,
            num2_str=request.num2,
            operation=request.operation
        )
        return ComplexArithmeticResponse(result=result, calculation=calc_str)
    except ValueError as e:
        # Catches validation, division by zero, etc.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
