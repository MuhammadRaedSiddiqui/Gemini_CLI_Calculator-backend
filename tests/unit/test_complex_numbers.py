import pytest
from app.services.complex_numbers import evaluate_complex_arithmetic
from app.models.complex_numbers import ComplexOperation

# --- Success Cases ---

def test_complex_addition():
    result, calc_str = evaluate_complex_arithmetic("1+2j", "3-4j", ComplexOperation.add)
    assert result == "4-2j"
    assert calc_str == "(1+2j) + (3-4j)"

def test_complex_subtraction():
    result, calc_str = evaluate_complex_arithmetic("5+5j", "1+2j", ComplexOperation.subtract)
    assert result == "4+3j"
    assert calc_str == "(5+5j) - (1+2j)"

def test_complex_multiplication():
    result, calc_str = evaluate_complex_arithmetic("1+2j", "3-4j", ComplexOperation.multiply)
    assert result == "11+2j"
    assert calc_str == "(1+2j) * (3-4j)"

def test_complex_division():
    result, calc_str = evaluate_complex_arithmetic("-2+6j", "2+2j", ComplexOperation.divide)
    assert result == "1+2j"
    assert calc_str == "(-2+6j) / (2+2j)"

def test_complex_real_result():
    # (1+j)(1-j) = 1 - (-1) = 2
    result, _ = evaluate_complex_arithmetic("1+1j", "1-1j", ComplexOperation.multiply)
    assert result == "2.0"

# --- Error Cases ---

def test_complex_division_by_zero_error():
    with pytest.raises(ValueError, match="Complex division by zero is not allowed"):
        evaluate_complex_arithmetic("1+1j", "0", ComplexOperation.divide)
    with pytest.raises(ValueError, match="Complex division by zero is not allowed"):
        evaluate_complex_arithmetic("3+4j", "0+0j", ComplexOperation.divide)

def test_invalid_complex_number_string_error():
    # The service layer relies on Python's `complex()` constructor, which will raise a ValueError.
    # The Pydantic model also validates this, but we test the service function directly here.
    with pytest.raises(ValueError):
        evaluate_complex_arithmetic("1+2i", "3-4j", ComplexOperation.add)
    with pytest.raises(ValueError):
        evaluate_complex_arithmetic("nota-number", "3-4j", ComplexOperation.multiply)
