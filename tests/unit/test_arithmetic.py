import pytest
from app.services.arithmetic import evaluate_arithmetic_expression

def test_evaluate_addition():
    assert evaluate_arithmetic_expression("1 + 1") == 2.0

def test_evaluate_subtraction():
    assert evaluate_arithmetic_expression("10 - 5") == 5.0

def test_evaluate_multiplication():
    assert evaluate_arithmetic_expression("4 * 5") == 20.0

def test_evaluate_division():
    assert evaluate_arithmetic_expression("20 / 4") == 5.0

def test_evaluate_complex_expression():
    assert evaluate_arithmetic_expression("(2 + 3) * 4") == 20.0

def test_evaluate_division_by_zero():
    # Sympy returns zoo for division by zero, which cannot be converted to float
    with pytest.raises(ValueError):
        evaluate_arithmetic_expression("1 / 0")

def test_evaluate_invalid_expression():
    with pytest.raises(ValueError):
        evaluate_arithmetic_expression("1 +")

def test_evaluate_malformed_expression_mismatched_parentheses():
    with pytest.raises(ValueError):
        evaluate_arithmetic_expression("(1 + 2")

def test_evaluate_double_plus_expression():
    # Sympy interprets "1 ++ 2" as 1 + (+2)
    assert evaluate_arithmetic_expression("1 ++ 2") == 3.0

def test_evaluate_empty_expression():
    with pytest.raises(ValueError):
        evaluate_arithmetic_expression("")

def test_evaluate_expression_with_letters():
    with pytest.raises(ValueError):
        evaluate_arithmetic_expression("a + b")
