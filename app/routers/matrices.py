from fastapi import APIRouter, HTTPException
from app.models.matrices import MatrixRequest, MatrixResponse
from app.services.matrices import perform_matrix_operation

router = APIRouter()

@router.post("/matrices/evaluate",
             response_model=MatrixResponse,
             tags=["Matrices"],
             summary="Perform a matrix operation (multiply, determinant, inverse)",
             description="""
Performs a specified operation on one or two matrices.

- **Operations**: `multiply`, `determinant`, `inverse`
- For `multiply`, both `matrix1` and `matrix2` are required.
- For `determinant` and `inverse`, only `matrix1` is required.
""")
async def evaluate_matrix_endpoint(request: MatrixRequest):
    """
    Endpoint to perform a matrix operation.

    - **request**: A `MatrixRequest` model.
    """
    try:
        result, shape1, shape2 = perform_matrix_operation(
            operation=request.operation,
            matrix1=request.matrix1,
            matrix2=request.matrix2
        )
        return MatrixResponse(
            result=result,
            operation=request.operation.value,
            input_shape1=shape1,
            input_shape2=shape2
        )
    except ValueError as e:
        # Catches errors from the service layer or Pydantic model validation
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # A catch-all for other unexpected server errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
