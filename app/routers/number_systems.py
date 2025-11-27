from fastapi import APIRouter, HTTPException
from app.models.number_systems import ConversionRequest, ConversionResponse
from app.services.number_systems import convert_number_system

router = APIRouter()

@router.post("/numbers/convert",
             response_model=ConversionResponse,
             tags=["Number Systems"],
             summary="Convert a number between different bases",
             description="""
Converts a number from a source base to a target base.

- **Bases**: `2` (Binary), `8` (Octal), `10` (Decimal), `16` (Hexadecimal).
- The input `value` must be a valid number string in the `from_base`.
""")
async def convert_number_endpoint(request: ConversionRequest):
    """
    Endpoint to convert a number between two bases.

    - **request**: A `ConversionRequest` model.
    """
    try:
        result = convert_number_system(
            value=request.value,
            from_base=request.from_base,
            to_base=request.to_base
        )
        return ConversionResponse(
            result=result,
            from_base=request.from_base,
            to_base=request.to_base,
            original_value=request.value
        )
    except ValueError as e:
        # Catches errors from the service layer or Pydantic model validation.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
