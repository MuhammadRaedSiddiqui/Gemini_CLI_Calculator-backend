import pytest
import numpy as np
from app.services.trigonometry import evaluate_trigonometric_function
from app.models.trigonometry import TrigonometricFunction, AngleUnit

# Using pytest.approx for floating point comparisons

# --- Test Standard Functions (sin, cos, tan) ---
def test_sin_radians():
    assert evaluate_trigonometric_function(TrigonometricFunction.sin, np.pi / 2, AngleUnit.radians) == pytest.approx(1.0)

def test_cos_radians():
    assert evaluate_trigonometric_function(TrigonometricFunction.cos, np.pi, AngleUnit.radians) == pytest.approx(-1.0)

def test_tan_radians():
    assert evaluate_trigonometric_function(TrigonometricFunction.tan, np.pi / 4, AngleUnit.radians) == pytest.approx(1.0)

def test_sin_degrees():
    assert evaluate_trigonometric_function(TrigonometricFunction.sin, 90, AngleUnit.degrees) == pytest.approx(1.0)

def test_cos_degrees():
    assert evaluate_trigonometric_function(TrigonometricFunction.cos, 180, AngleUnit.degrees) == pytest.approx(-1.0)

def test_tan_degrees():
    assert evaluate_trigonometric_function(TrigonometricFunction.tan, 45, AngleUnit.degrees) == pytest.approx(1.0)


# --- Test Inverse Functions (asin, acos, atan) ---
def test_asin_radians():
    assert evaluate_trigonometric_function(TrigonometricFunction.asin, 1, AngleUnit.radians) == pytest.approx(np.pi / 2)

def test_acos_degrees():
    # Result should be in degrees
    assert evaluate_trigonometric_function(TrigonometricFunction.acos, -1, AngleUnit.degrees) == pytest.approx(180)

def test_atan_degrees():
    assert evaluate_trigonometric_function(TrigonometricFunction.atan, 1, AngleUnit.degrees) == pytest.approx(45)


# --- Test Hyperbolic Functions (sinh, cosh, tanh) ---
def test_sinh():
    # Hyperbolic functions don't use angle units, but the model requires it. Radians is neutral.
    assert evaluate_trigonometric_function(TrigonometricFunction.sinh, 0, AngleUnit.radians) == pytest.approx(0.0)
    assert evaluate_trigonometric_function(TrigonometricFunction.sinh, 1, AngleUnit.degrees) > 1.17

def test_cosh():
    assert evaluate_trigonometric_function(TrigonometricFunction.cosh, 0, AngleUnit.radians) == pytest.approx(1.0)
    assert evaluate_trigonometric_function(TrigonometricFunction.cosh, 1, AngleUnit.degrees) > 1.54

# --- Test Domain and Edge Case Errors ---
def test_asin_domain_error():
    """ Test asin with an input outside the valid domain of [-1, 1]. """
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_trigonometric_function(TrigonometricFunction.asin, 1.1, AngleUnit.radians)

def test_acos_domain_error():
    """ Test acos with an input outside the valid domain of [-1, 1]. """
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_trigonometric_function(TrigonometricFunction.acos, -2, AngleUnit.degrees)

def test_acosh_domain_error():
    """ Test acosh with an input outside the valid domain of [1, inf). """
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_trigonometric_function(TrigonometricFunction.acosh, 0.5, AngleUnit.radians)

def test_atanh_domain_error():
    """ Test atanh with an input outside the valid domain of (-1, 1). """
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_trigonometric_function(TrigonometricFunction.atanh, 1, AngleUnit.radians)

def test_tan_90_degrees_is_large():
    """ 
    tan(90) is technically infinite. Numpy returns a very large number instead of raising an error.
    This test asserts that the result is large, which is the expected behavior from the backend.
    """
    result = evaluate_trigonometric_function(TrigonometricFunction.tan, 90, AngleUnit.degrees)
    assert abs(result) > 1e16 # Check for a very large number
