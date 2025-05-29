"""MODULE for computing sin using math lib and Taylor series"""

import math
from functools import wraps
from typing import List, Tuple


def taylor_sin(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int]:
    """
    Computes sine using Taylor series expansion.

    Args:
        x: Input value in radians
        eps: Required precision
        max_iter: Maximum iterations allowed

    Returns:
        Tuple of (approximate sine value, terms used)
    """
    term = x  # First term
    sum_sin = term
    n = 1

    while abs(term) > eps and n < max_iter:
        term *= -x ** 2 / ((2 * n) * (2 * n + 1))
        sum_sin += term
        n += 1

    return sum_sin, n

def validate_input(func):
    """
    Decorator to validate function inputs.
    Ensures positive epsilon and handles value errors.
    """

    @wraps(func) # Saves the metadata of the function
    def wrapper(*args, **kwargs):
        try:
            x = float(input("Enter x (in radians): "))
            eps = float(input("Enter precision (epsilon): "))
            if eps <= 0:
                raise ValueError("Epsilon must be positive.")
            return func(x, eps, *args, **kwargs)
        except ValueError as e:
            print(f"Invalid input: {e}")
            return None
    return wrapper


@validate_input
def compute_and_compare_sin(x: float, eps: float):
    """
    Computes and compares Taylor series approximation with math.sin

    Args:
        x: Input value in radians
        eps: Required precision
    """
    approx_sin, terms = taylor_sin(x, eps)
    exact_sin = math.sin(x)

    print("\n|    x    |   n   |    F(x)   | Math F(x) |    eps    |")
    print("-" * 50)
    print(f"| {x:^6.3f} | {terms:^5} | {approx_sin:^9.6f} | {exact_sin:^9.6f} | {eps:^9.1e} |")

