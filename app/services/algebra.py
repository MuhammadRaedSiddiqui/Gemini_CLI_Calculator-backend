import numpy as np
from typing import List, Tuple

def _format_polynomial(coeffs: List[float]) -> str:
    """
    Helper to create a user-friendly string representation of the polynomial.
    Example: [1, 0, -4] -> "x**2 - 4.0"
    """
    if all(c == 0 for c in coeffs):
        return "0"

    poly_str_parts = []
    degree = len(coeffs) - 1
    for i, coeff in enumerate(coeffs):
        if np.isclose(coeff, 0):
            continue

        power = degree - i
        
        sign = " - " if coeff < 0 else " + "
        
        coeff_abs = abs(coeff)

        if i == 0 or not poly_str_parts:
            sign = "-" if coeff < 0 else ""
        
        coeff_str = "" if np.isclose(coeff_abs, 1) and power > 0 else f"{coeff_abs:.1f}".replace(".0", "")

        if power == 0:
            var_str = ""
        elif power == 1:
            var_str = "x"
        else:
            var_str = f"x**{power}"

        term = f"{coeff_str}{'*' if coeff_str and var_str else ''}{var_str}"
        
        poly_str_parts.append(f"{sign}{term}")
        
    return "".join(poly_str_parts).lstrip(" +")

def solve_polynomial_roots(coefficients: List[float]) -> Tuple[List[str], str]:
    """
    Finds the roots of a polynomial given its coefficients.
    """
    if len(coefficients) < 2:
        raise ValueError("At least two coefficients are required for a polynomial of degree >= 1.")

    polynomial_str = _format_polynomial(coefficients)
    
    roots = np.roots(coefficients)
    
    formatted_roots = []
    for root in roots:
        if np.isclose(root.imag, 0):
            formatted_roots.append(f"{root.real:.4f}")
        else:
            real_part = 0.0 if np.isclose(root.real, 0) else root.real
            formatted_roots.append(f"{real_part:.4f}{root.imag:+.4f}j")
            
    return formatted_roots, polynomial_str
