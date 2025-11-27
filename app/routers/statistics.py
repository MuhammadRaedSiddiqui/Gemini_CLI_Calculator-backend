from fastapi import APIRouter, HTTPException
from app.models.statistics import StatisticsRequest, StatisticsResponse
from app.services.statistics import perform_statistics_operation

router = APIRouter()

@router.post("/statistics/evaluate",
             response_model=StatisticsResponse,
             tags=["Statistics"],
             summary="Perform a statistical calculation on a dataset",
             description="""
Calculates the mean, median, standard deviation, or variance for a given list of numbers.

- **Operations**: `mean`, `median`, `std_dev`, `variance`
- **data**: A list containing at least one number.
""")
async def evaluate_statistics_endpoint(request: StatisticsRequest):
    """
    Endpoint to perform a statistical calculation.

    - **request**: A `StatisticsRequest` model.
    """
    try:
        result = perform_statistics_operation(
            operation=request.operation,
            data=request.data
        )
        return StatisticsResponse(
            result=result,
            operation=request.operation.value,
            dataset_size=len(request.data)
        )
    except ValueError as e:
        # Catches errors from the service layer, e.g., empty dataset
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
