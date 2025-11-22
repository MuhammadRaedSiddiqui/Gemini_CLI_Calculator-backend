import numpy as np
from app.models.trigonometry import TrigonometricFunction, AngleUnit

def evaluate_trigonometric_function(function: TrigonometricFunction, value: float, unit: AngleUnit) -> float:
    """
    Evaluates a trigonometric function using numpy.

    Args:
        function: The trigonometric function to evaluate (e.g., sin, cos, tan).
        value: The input value (angle or number).
        unit: The angle unit, 'radians' or 'degrees'.

    Returns:
        The result of the trigonometric calculation.

    Raises:
        ValueError: If the function is not supported, or if the input value is
                    outside the valid domain for the function (e.g., asin(1.1)).
    """
    input_for_calc = value
    # Convert degrees to radians for standard trig functions, which expect radians
    if unit == AngleUnit.degrees and function in [
        TrigonometricFunction.sin, TrigonometricFunction.cos, TrigonometricFunction.tan
    ]:
        input_for_calc = np.deg2rad(value)

    # Map function enums to their corresponding numpy implementations
    func_map = {
        TrigonometricFunction.sin: np.sin,
        TrigonometricFunction.cos: np.cos,
        TrigonometricFunction.tan: np.tan,
        TrigonometricFunction.asin: np.arcsin,
        TrigonometricFunction.acos: np.arccos,
        TrigonometricFunction.atan: np.arctan,
        TrigonometricFunction.sinh: np.sinh,
        TrigonometricFunction.cosh: np.cosh,
        TrigonometricFunction.tanh: np.tanh,
        TrigonometricFunction.asinh: np.arcsinh,
        TrigonometricFunction.acosh: np.arccosh,
        TrigonometricFunction.atanh: np.arctanh,
    }

    if function not in func_map:
        raise ValueError(f"Unsupported trigonometric function: {function}")

    # Perform the calculation within an errstate context to suppress warnings
    with np.errstate(divide='ignore', invalid='ignore'):
        try:
            result = func_map[function](input_for_calc)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Calculation error for {function}({value}): {e}")

    # For inverse functions (like asin, acos, atan), the result is in radians.
    # Convert back to degrees if the user requested degrees.
    if unit == AngleUnit.degrees and function in [
        TrigonometricFunction.asin, TrigonometricFunction.acos, TrigonometricFunction.atan
    ]:
        result = np.rad2deg(result)

    # Check for NaN or infinity, which indicate domain errors
    if np.isnan(result) or np.isinf(result):
        raise ValueError(f"Domain error: The input '{value}' is outside the valid domain for the function '{function}'.")

    return float(result)
