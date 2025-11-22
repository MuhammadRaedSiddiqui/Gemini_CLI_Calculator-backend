from app.models.complex_numbers import ComplexOperation

def evaluate_complex_arithmetic(num1_str: str, num2_str: str, operation: ComplexOperation) -> tuple[str, str]:
    """
    Performs arithmetic (add, subtract, multiply, divide) on two complex numbers.

    Args:
        num1_str: The first complex number as a string (e.g., "3+4j").
        num2_str: The second complex number as a string (e.g., "1-2j").
        operation: The operation to perform.

    Returns:
        A tuple containing the formatted result string and the calculation string.
        
    Raises:
        ValueError: If the operation is invalid or division by zero occurs.
    """
    # The Pydantic model already validates the strings, but we convert them here.
    c1 = complex(num1_str)
    c2 = complex(num2_str)

    op_map = {
        ComplexOperation.add: (lambda a, b: a + b, "+"),
        ComplexOperation.subtract: (lambda a, b: a - b, "-"),
        ComplexOperation.multiply: (lambda a, b: a * b, "*"),
        ComplexOperation.divide: (lambda a, b: a / b, "/"),
    }

    if operation not in op_map:
        # This should be unreachable if using the Enum
        raise ValueError(f"Unsupported operation: {operation}")

    if operation == ComplexOperation.divide and c2 == 0:
        raise ValueError("Complex division by zero is not allowed.")

    func, op_symbol = op_map[operation]
    result = func(c1, c2)

    def format_complex_result(c: complex) -> str:
        """Formats a complex number into a clean string like '11+2j' or '5.5'."""
        if c.imag == 0:
            return str(c.real)
        # Python's default str() for complex numbers includes parentheses, e.g., '(11+2j)'
        # We remove them for a cleaner calculator-style output.
        return str(c).replace("(", "").replace(")", "")

    result_str = format_complex_result(result)
    calculation_str = f"({num1_str}) {op_symbol} ({num2_str})"
    
    return result_str, calculation_str
