from app.models.number_systems import NumberSystem

def convert_number_system(value: str, from_base: NumberSystem, to_base: NumberSystem) -> str:
    """
    Converts a number string from a source base to a target base.

    Args:
        value: The number string to convert.
        from_base: The base of the input number.
        to_base: The target base for the conversion.

    Returns:
        The converted number as a string.
        
    Raises:
        ValueError: If the input value is not valid for the source base or
                    if the target base is unsupported.
    """
    try:
        # First, convert the input string from its base to a standard decimal integer.
        # The `int()` function with a base argument is perfect for this.
        decimal_value = int(value, from_base)
    except ValueError:
        # This is a safeguard, as the Pydantic model should have already validated this.
        raise ValueError(f"Invalid number '{value}' for base {from_base}.")

    # Now, convert the decimal integer to the target base string representation.
    if to_base == NumberSystem.BINARY:
        # `bin()` returns a string like '0b101', so we slice off the prefix.
        return bin(decimal_value)[2:]
    elif to_base == NumberSystem.OCTAL:
        # `oct()` returns '0o77', so we slice.
        return oct(decimal_value)[2:]
    elif to_base == NumberSystem.HEXADECIMAL:
        # `hex()` returns '0xff', so we slice and convert to uppercase for consistency.
        return hex(decimal_value)[2:].upper()
    elif to_base == NumberSystem.DECIMAL:
        return str(decimal_value)
    else:
        # This case should be unreachable with the NumberSystem Enum.
        raise ValueError(f"Unsupported target base: {to_base}")
