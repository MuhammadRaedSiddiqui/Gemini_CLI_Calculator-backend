from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import List, Optional, Union

class MatrixOperation(str, Enum):
    multiply = "multiply"
    determinant = "determinant"
    inverse = "inverse"

class MatrixRequest(BaseModel):
    operation: MatrixOperation
    matrix1: List[List[float]] = Field(..., json_schema_extra={'example': [[1, 2], [3, 4]]})
    matrix2: Optional[List[List[float]]] = Field(None, json_schema_extra={'example': [[5, 6], [7, 8]]})

    @model_validator(mode='after')
    def validate_request(self):
        op = self.operation
        m1 = self.matrix1
        m2 = self.matrix2

        if op == MatrixOperation.multiply and m2 is None:
            raise ValueError("`matrix2` is required for multiplication.")
        
        if op in [MatrixOperation.determinant, MatrixOperation.inverse] and m2 is not None:
            raise ValueError(f"`matrix2` should not be provided for {op.value}.")
            
        # Basic validation for matrix shape
        if m1:
            first_row_len = len(m1[0])
            if not all(len(row) == first_row_len for row in m1):
                raise ValueError("All rows in `matrix1` must have the same length.")

        if m2:
            first_row_len = len(m2[0])
            if not all(len(row) == first_row_len for row in m2):
                raise ValueError("All rows in `matrix2` must have the same length.")

        return self

class MatrixResponse(BaseModel):
    # The result can be a matrix (list of lists) or a single number (determinant)
    result: Union[List[List[float]], float]
    operation: str
    input_shape1: str
    input_shape2: Optional[str] = None
