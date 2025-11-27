from pydantic import BaseModel, Field

class ArithmeticRequest(BaseModel):
    expression: str = Field(..., json_schema_extra={'example': "2 * (3 + 4)"})

class ArithmeticResponse(BaseModel):
    result: float
    expression: str
