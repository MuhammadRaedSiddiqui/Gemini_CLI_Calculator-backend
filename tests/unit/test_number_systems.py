import pytest
from app.services.number_systems import convert_number_system
from app.models.number_systems import NumberSystem

# --- Test conversions from DECIMAL ---
def test_decimal_to_binary():
    assert convert_number_system("10", NumberSystem.DECIMAL, NumberSystem.BINARY) == "1010"

def test_decimal_to_octal():
    assert convert_number_system("10", NumberSystem.DECIMAL, NumberSystem.OCTAL) == "12"

def test_decimal_to_hex():
    assert convert_number_system("255", NumberSystem.DECIMAL, NumberSystem.HEXADECIMAL) == "FF"

# --- Test conversions TO DECIMAL ---
def test_binary_to_decimal():
    assert convert_number_system("1101", NumberSystem.BINARY, NumberSystem.DECIMAL) == "13"

def test_octal_to_decimal():
    assert convert_number_system("77", NumberSystem.OCTAL, NumberSystem.DECIMAL) == "63"

def test_hex_to_decimal():
    assert convert_number_system("1A", NumberSystem.HEXADECIMAL, NumberSystem.DECIMAL) == "26"
    assert convert_number_system("ff", NumberSystem.HEXADECIMAL, NumberSystem.DECIMAL) == "255"

# --- Test conversions between non-decimal bases ---
def test_hex_to_binary():
    assert convert_number_system("FF", NumberSystem.HEXADECIMAL, NumberSystem.BINARY) == "11111111"

def test_binary_to_octal():
    assert convert_number_system("101010", NumberSystem.BINARY, NumberSystem.OCTAL) == "52"

# --- Test error cases ---
def test_invalid_value_for_binary_base():
    with pytest.raises(ValueError, match="Invalid number '123' for base 2"):
        convert_number_system("123", NumberSystem.BINARY, NumberSystem.DECIMAL)

def test_invalid_value_for_hex_base():
    # 'G' is not a valid hexadecimal character
    with pytest.raises(ValueError, match="Invalid number 'G' for base 16"):
        convert_number_system("G", NumberSystem.HEXADECIMAL, NumberSystem.DECIMAL)
