from pydantic import BaseModel, Field, conlist
from enum import Enum
from typing import List

class StatisticsOperation(str, Enum):
    mean = "mean"
    median = "median"
    std_dev = "std_dev"
    variance = "variance"

class StatisticsRequest(BaseModel):
    operation: StatisticsOperation
    # Use conlist to enforce at least one number in the dataset
    data: conlist(float, min_length=1) = Field(..., json_schema_extra={'example': [1, 2, 3, 4, 5]})

class StatisticsResponse(BaseModel):
    result: float
    operation: str
    dataset_size: int
