from pydantic import BaseModel, Field, field_validator
from enum import IntEnum

class NumberSystem(IntEnum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEXADECIMAL = 16

class ConversionRequest(BaseModel):
    value: str = Field(..., description="The number to convert, represented as a string.", json_schema_extra={'example': "FF"})
    from_base: NumberSystem = Field(..., description="The base of the input number.")
    to_base: NumberSystem = Field(..., description="The target base to convert to.")

    @field_validator('value')
    def validate_value_for_base(cls, v, values):
        if 'from_base' in values.data:
            from_base = values.data['from_base']
            try:
                # Check if the value is valid for the given base
                int(v, from_base)
            except ValueError:
                raise ValueError(f"Value '{v}' is not a valid number in base {from_base}.")
        return v

class ConversionResponse(BaseModel):
    result: str
    from_base: int
    to_base: int
    original_value: str
