from sympy import sympify, diff, integrate, Symbol, SympifyError
from sympy.core.numbers import Number
from typing import Optional, Tuple
from app.models.calculus import CalculusOperation

def perform_calculus_operation(
    expression_str: str,
    operation: CalculusOperation,
    bounds: Optional[Tuple[float, float]] = None
) -> Tuple[str, bool]:
    """
    Performs a calculus operation (differentiation or integration) on an expression.
    """
    try:
        x = Symbol('x')
        # Use a limited local namespace for safety
        expr = sympify(expression_str, locals={'x': x})
    except (SympifyError, TypeError) as e:
        raise ValueError(f"Invalid expression: '{expression_str}'. Error: {e}")

    is_definite = False
    if operation == CalculusOperation.differentiate:
        result = diff(expr, x)
    elif operation == CalculusOperation.integrate:
        if bounds:
            # Definite integral
            is_definite = True
            lower_bound, upper_bound = bounds
            result = integrate(expr, (x, lower_bound, upper_bound))
        else:
            # Indefinite integral
            result = integrate(expr, x)
    else:
        # Should not be reachable with Enum validation
        raise ValueError(f"Invalid calculus operation: {operation}")

    # Format numeric results cleanly
    if isinstance(result, Number):
        # Format to a reasonable precision, then strip trailing zeros and decimal point if possible
        result_str = f"{float(result):.10f}".rstrip('0').rstrip('.')
        return result_str, is_definite

    return str(result), is_definite
