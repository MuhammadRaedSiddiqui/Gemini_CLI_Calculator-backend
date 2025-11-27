import pytest
import numpy as np
from app.services.algebra import solve_polynomial_roots, _format_polynomial

# --- Tests for the _format_polynomial helper function ---

def test_format_simple_linear():
    assert _format_polynomial([1, -4]) == "x - 4"
    assert _format_polynomial([2, 4]) == "2*x + 4"

def test_format_quadratic():
    assert _format_polynomial([1, -3, 2]) == "x**2 - 3*x + 2"
    assert _format_polynomial([-1, 0, 4]) == "-x**2 + 4"

def test_format_higher_degree():
    assert _format_polynomial([2, 0, -3, 1]) == "2*x**3 - 3*x + 1"

def test_format_all_zeros():
    assert _format_polynomial([0, 0, 0]) == "0"

def test_format_single_term():
    assert _format_polynomial([4, 0, 0]) == "4*x**2"


# --- Tests for the main solve_polynomial_roots service function ---

def test_solve_linear_equation():
    # 2x - 4 = 0  => x = 2
    roots, poly_str = solve_polynomial_roots([2, -4])
    assert len(roots) == 1
    assert roots[0] == "2.0000"
    assert poly_str == "2*x - 4"

def test_solve_quadratic_with_real_roots():
    # x^2 - 3x + 2 = 0 => (x-1)(x-2) => roots are 1, 2
    roots, poly_str = solve_polynomial_roots([1, -3, 2])
    assert len(roots) == 2
    # Order of roots is not guaranteed
    assert "1.0000" in roots
    assert "2.0000" in roots
    assert poly_str == "x**2 - 3*x + 2"

def test_solve_quadratic_with_complex_roots():
    # x^2 + 1 = 0 => roots are i, -i
    roots, poly_str = solve_polynomial_roots([1, 0, 1])
    assert len(roots) == 2
    assert "0.0000+1.0000j" in roots
    assert "0.0000-1.0000j" in roots
    assert poly_str == "x**2 + 1"

def test_solve_cubic_equation():
    # x^3 - 6x^2 + 11x - 6 = 0 => (x-1)(x-2)(x-3) => roots 1, 2, 3
    roots, poly_str = solve_polynomial_roots([1, -6, 11, -6])
    assert len(roots) == 3
    assert "1.0000" in roots
    assert "2.0000" in roots
    assert "3.0000" in roots

# --- Error Case ---
def test_insufficient_coefficients_error():
    """ Test that the service raises an error if fewer than 2 coefficients are provided. """
    with pytest.raises(ValueError, match="At least two coefficients are required"):
        solve_polynomial_roots([5])
    with pytest.raises(ValueError, match="At least two coefficients are required"):
        solve_polynomial_roots([])
