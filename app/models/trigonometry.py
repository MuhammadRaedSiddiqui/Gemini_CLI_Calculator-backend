from pydantic import BaseModel, Field
from enum import Enum

class TrigonometricFunction(str, Enum):
    sin = "sin"
    cos = "cos"
    tan = "tan"
    asin = "asin"
    acos = "acos"
    atan = "atan"
    sinh = "sinh"
    cosh = "cosh"
    tanh = "tanh"
    asinh = "asinh"
    acosh = "acosh"
    atanh = "atanh"

class AngleUnit(str, Enum):
    radians = "radians"
    degrees = "degrees"

class TrigonometryRequest(BaseModel):
    function: TrigonometricFunction = Field(..., json_schema_extra={'example': "sin"})
    value: float = Field(..., json_schema_extra={'example': 1.5708})
    unit: AngleUnit = Field(AngleUnit.radians, json_schema_extra={'example': "radians"})

class TrigonometryResponse(BaseModel):
    result: float
    function: str
    input_value: float
    unit: str
