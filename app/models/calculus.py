from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional, Tuple

class CalculusOperation(str, Enum):
    differentiate = "differentiate"
    integrate = "integrate"

class CalculusRequest(BaseModel):
    expression: str = Field(..., description="The mathematical expression to operate on, using 'x' as the variable.", json_schema_extra={'example': "x**2"})
    operation: CalculusOperation
    # For definite integrals: a tuple of (lower_bound, upper_bound)
    integration_bounds: Optional[Tuple[float, float]] = Field(None, description="[For Definite Integrals Only] A tuple for the lower and upper bounds.", json_schema_extra={'example': (0, 1)})

    @model_validator(mode='after')
    def validate_request(self):
        if self.operation == CalculusOperation.differentiate and self.integration_bounds is not None:
            raise ValueError("`integration_bounds` must not be provided for differentiation.")
        return self

class CalculusResponse(BaseModel):
    result: str = Field(..., description="The resulting expression (for indefinite integrals/derivatives) or numerical value (for definite integrals).")
    input_expression: str
    operation: str
    is_definite_integral: bool = False
