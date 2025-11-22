from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import Enum

class LogarithmicFunction(str, Enum):
    ln = "ln"      # Natural logarithm (base e)
    log10 = "log10"  # Common logarithm (base 10)
    log = "log"      # Logarithm with a custom base

class LogarithmRequest(BaseModel):
    function: LogarithmicFunction = Field(..., json_schema_extra={'example': "log"})
    value: float = Field(..., json_schema_extra={'example': 1024})
    base: Optional[float] = Field(None, description="Required if function is 'log'", json_schema_extra={'example': 2})

    @model_validator(mode='after')
    def check_base_for_log(self):
        if self.function == LogarithmicFunction.log and self.base is None:
            raise ValueError("`base` is required for the 'log' function.")
        if self.function != LogarithmicFunction.log and self.base is not None:
            raise ValueError(f"`base` should not be provided for the '{self.function}' function.")
        return self

class LogarithmResponse(BaseModel):
    result: float
    function: str
    input_value: float
    base: Optional[float] = None
