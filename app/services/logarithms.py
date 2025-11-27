import numpy as np
from typing import Optional
from app.models.logarithms import LogarithmicFunction

def evaluate_logarithmic_function(function: LogarithmicFunction, value: float, base: Optional[float] = None) -> float:
    """
    Evaluates a logarithmic function using numpy.

    Args:
        function: The logarithmic function to evaluate ('ln', 'log10', 'log').
        value: The input value for the logarithm.
        base: The base of the logarithm. Required only for the 'log' function.

    Returns:
        The result of the calculation.

    Raises:
        ValueError: If there are domain errors (e.g., log of a negative number),
                    if the base is invalid, or for other calculation issues.
    """
    # Use errstate to handle numpy warnings for domain errors (e.g., log(0))
    with np.errstate(divide='ignore', invalid='ignore'):
        if function == LogarithmicFunction.ln:
            result = np.log(value)
        elif function == LogarithmicFunction.log10:
            result = np.log10(value)
        elif function == LogarithmicFunction.log:
            # This check is redundant if Pydantic model is used, but good for service-layer integrity
            if base is None:
                raise ValueError("A `base` must be provided for the 'log' function.")
            if base <= 0 or base == 1:
                raise ValueError("Logarithm base must be positive and not equal to 1.")
            # Calculate log with custom base using the change of base formula
            result = np.log(value) / np.log(base)
        else:
            # This case should not be reachable if using the Enum
            raise ValueError(f"Unsupported logarithmic function: {function}")

    # Check for NaN or infinity, which signal a domain error has occurred
    if np.isnan(result) or np.isinf(result):
        raise ValueError(
            f"Domain error: Invalid `value` '{value}' or `base` '{base}' for function '{function}'. "
            "Logarithm requires a positive value and, if applicable, a positive base not equal to 1."
        )

    return float(result)
