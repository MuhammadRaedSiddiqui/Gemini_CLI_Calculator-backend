from pydantic import BaseModel, Field, conlist
from typing import List, Union

class PolynomialSolverRequest(BaseModel):
    # Use conlist to ensure there's at least one coefficient
    coefficients: conlist(float, min_length=1) = Field(
        ...,
        description="List of polynomial coefficients in descending order of power (e.g., [1, -3, 2] for x^2 - 3x + 2).",
        json_schema_extra={'example': [1, 0, -4]} # x^2 - 4
    )

class PolynomialSolverResponse(BaseModel):
    roots: List[str] = Field(
        ...,
        description="List of roots (solutions) of the polynomial. Complex roots are returned as strings.",
        json_schema_extra={'example': ["2.0", "-2.0"]}
    )
    polynomial: str = Field(
        ...,
        description="A string representation of the polynomial.",
        json_schema_extra={'example': "1.0*x**2 - 4.0"}
    )
