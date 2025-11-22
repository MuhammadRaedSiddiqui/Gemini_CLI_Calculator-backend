from fastapi import APIRouter, HTTPException
from app.models.algebra import PolynomialSolverRequest, PolynomialSolverResponse
from app.services.algebra import solve_polynomial_roots

router = APIRouter()

@router.post("/algebra/poly-solve",
             response_model=PolynomialSolverResponse,
             tags=["Algebra"],
             summary="Solve a polynomial equation by finding its roots",
             description="""
Finds the roots of a polynomial equation given its coefficients.
The coefficients should be provided in a list in descending order of power.

**Example:** For the equation `x^2 - 4 = 0`, the coefficients are `[1, 0, -4]`.
The endpoint will return the roots `["2.0", "-2.0"]`.
""")
async def solve_polynomial_endpoint(request: PolynomialSolverRequest):
    """
    Endpoint to solve a polynomial by finding its roots.

    - **request**: A `PolynomialSolverRequest` model containing:
        - `coefficients`: A list of floats representing the polynomial.
    """
    try:
        roots, polynomial_str = solve_polynomial_roots(request.coefficients)
        return PolynomialSolverResponse(
            roots=roots,
            polynomial=polynomial_str
        )
    except ValueError as e:
        # Catches errors from the service layer, like not enough coefficients
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
