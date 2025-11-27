from pydantic import BaseModel, Field, field_validator
from enum import Enum

class ComplexOperation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"

class ComplexArithmeticRequest(BaseModel):
    num1: str = Field(..., description="First complex number in 'a+bj' format.", json_schema_extra={'example': "3+4j"})
    num2: str = Field(..., description="Second complex number in 'a+bj' format.", json_schema_extra={'example': "1-2j"})
    operation: ComplexOperation = Field(..., json_schema_extra={'example': "multiply"})

    @field_validator('num1', 'num2')
    def validate_complex_string(cls, v):
        try:
            complex(v)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid complex number format. Use 'a+bj' or 'a-bj'.")
        return v

class ComplexArithmeticResponse(BaseModel):
    result: str = Field(..., description="The result of the complex number operation.", json_schema_extra={'example': "11+2j"})
    calculation: str = Field(..., description="A string showing the calculation that was performed.", json_schema_extra={'example': "(3+4j) * (1-2j)"})
