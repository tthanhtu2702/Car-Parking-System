"""
check_digit_utils.py

Provides a utility function to calculate the Modulo 11 check digit.
"""

from typing import Union

def generate_mod11_digit(number: str) -> Union[int, str]:
    """
    Calculate Modulo 11 check digit.

    Args:
        number (str): A numeric string (usually 4 digits).

    Returns:
        Union[int, str]: The check digit (0–9), or 'X' if result exceeds 9.

    Raises:
        ValueError: If input is not a string of digits.
    """
    if not number.isdigit():
        raise ValueError("Input must be a numeric string.")

    weights = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    total = sum(int(d) * w for d, w in zip(reversed(number), weights))
    remainder = total % 11
    check_digit = 11 - remainder if remainder != 0 else 0
    return check_digit if check_digit < 10 else 'X'
