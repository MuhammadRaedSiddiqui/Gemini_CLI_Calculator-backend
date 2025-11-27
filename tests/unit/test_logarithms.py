import pytest
import numpy as np
from app.services.logarithms import evaluate_logarithmic_function
from app.models.logarithms import LogarithmicFunction

# --- Success Cases ---
def test_ln_success():
    assert evaluate_logarithmic_function(LogarithmicFunction.ln, np.e) == pytest.approx(1.0)
    assert evaluate_logarithmic_function(LogarithmicFunction.ln, 1) == pytest.approx(0.0)

def test_log10_success():
    assert evaluate_logarithmic_function(LogarithmicFunction.log10, 100) == pytest.approx(2.0)
    assert evaluate_logarithmic_function(LogarithmicFunction.log10, 1) == pytest.approx(0.0)

def test_log_custom_base_success():
    assert evaluate_logarithmic_function(LogarithmicFunction.log, 8, base=2) == pytest.approx(3.0)
    assert evaluate_logarithmic_function(LogarithmicFunction.log, 1, base=5) == pytest.approx(0.0)
    assert evaluate_logarithmic_function(LogarithmicFunction.log, 1000, base=10) == pytest.approx(3.0)


# --- Domain Error Cases (Invalid Value) ---
def test_log_zero_value_domain_error():
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_logarithmic_function(LogarithmicFunction.ln, 0)

def test_log_negative_value_domain_error():
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_logarithmic_function(LogarithmicFunction.log10, -100)

def test_custom_log_negative_value_domain_error():
    with pytest.raises(ValueError, match="Domain error"):
        evaluate_logarithmic_function(LogarithmicFunction.log, -8, base=2)


# --- Invalid Base Error Cases ---
def test_log_base_one_error():
    with pytest.raises(ValueError, match="Logarithm base must be positive and not equal to 1"):
        evaluate_logarithmic_function(LogarithmicFunction.log, 10, base=1)

def test_log_base_zero_error():
    with pytest.raises(ValueError, match="Logarithm base must be positive and not equal to 1"):
        evaluate_logarithmic_function(LogarithmicFunction.log, 10, base=0)

def test_log_base_negative_error():
    with pytest.raises(ValueError, match="Logarithm base must be positive and not equal to 1"):
        evaluate_logarithmic_function(LogarithmicFunction.log, 10, base=-2)


# --- Configuration Error Cases ---
def test_missing_base_for_log_error():
    """ Test that the service layer enforces the base requirement for 'log' function. """
    with pytest.raises(ValueError, match="A `base` must be provided for the 'log' function"):
        evaluate_logarithmic_function(LogarithmicFunction.log, 10)
