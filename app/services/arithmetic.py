from sympy import sympify, SympifyError

def evaluate_arithmetic_expression(expression: str) -> float:
    """
    Evaluates a simple arithmetic expression using SymPy's sympify.

    Args:
        expression: The arithmetic expression string.

    Returns:
        The result of the calculation.

    Raises:
        ValueError: If the expression is invalid or cannot be evaluated.
    """
    try:
        # Sympify the expression and evaluate it
        # We limit the locals/globals to prevent arbitrary code execution
        result = float(sympify(expression, locals={}).evalf())
        return result
    except (SympifyError, TypeError, ValueError) as e:
        raise ValueError(f"Invalid or malformed expression: {expression}. Error: {e}")
