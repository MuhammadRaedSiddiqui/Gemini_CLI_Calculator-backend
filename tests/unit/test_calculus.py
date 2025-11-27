import pytest
import numpy as np
from app.services.calculus import perform_calculus_operation
from app.models.calculus import CalculusOperation

# --- Test Differentiation ---
def test_differentiate_power_rule():
    result, is_definite = perform_calculus_operation("x**3", CalculusOperation.differentiate)
    assert result == "3*x**2"
    assert not is_definite

def test_differentiate_polynomial():
    result, _ = perform_calculus_operation("x**2 + 2*x + 1", CalculusOperation.differentiate)
    assert result == "2*x + 2"

def test_differentiate_trig_function():
    result, _ = perform_calculus_operation("sin(x)", CalculusOperation.differentiate)
    assert result == "cos(x)"


# --- Test Indefinite Integration ---
def test_integrate_indefinite_power_rule():
    result, is_definite = perform_calculus_operation("3*x**2", CalculusOperation.integrate)
    assert result == "x**3"
    assert not is_definite

def test_integrate_indefinite_polynomial():
    # Sympy does not add the constant of integration "+ C", which is acceptable.
    result, _ = perform_calculus_operation("2*x + 2", CalculusOperation.integrate)
    assert result == "x**2 + 2*x"

def test_integrate_indefinite_trig_function():
    result, _ = perform_calculus_operation("cos(x)", CalculusOperation.integrate)
    assert result == "sin(x)"


# --- Test Definite Integration ---
def test_integrate_definite_polynomial():
    result, is_definite = perform_calculus_operation("2*x", CalculusOperation.integrate, bounds=(0, 1))
    assert result == "1"
    assert is_definite

def test_integrate_definite_trig_function():
    # Integrate sin(x) from 0 to pi
    result, _ = perform_calculus_operation("sin(x)", CalculusOperation.integrate, bounds=(0, np.pi))
    # The result of the definite integral of sin(x) from 0 to pi is 2.
    assert pytest.approx(float(result)) == 2.0


# --- Test Error Handling ---
def test_invalid_expression_error():
    with pytest.raises(ValueError, match="Invalid expression"):
        perform_calculus_operation("log(x", CalculusOperation.differentiate)

def test_unsupported_operation_in_service():
    # This case should be prevented by the Enum in the model, but we test the service defense.
    with pytest.raises(ValueError, match="Invalid calculus operation"):
        perform_calculus_operation("x**2", "unsupported_op")
