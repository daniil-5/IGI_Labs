import math
from functools import wraps
from typing import Tuple, List, Callable


def validate_input(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            x = float(input("Enter x in radians: "))
            eps = float(input("Enter precision (ε > 0): "))
            if eps <= 0:
                raise ValueError("ε must be positive")
            return func(x, eps, *args, **kwargs)
        except ValueError as e:
            print(f"Error: {e}")
            return None

    return wrapper

class TaylorSin:
    @staticmethod
    def taylor_sin(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int]:
        term = x
        sum_sin = term
        n = 1

        while abs(term) > eps and n < max_iter:
            term *= -x ** 2 / ((2 * n) * (2 * n + 1))
            sum_sin += term
            n += 1

        return sum_sin, n

    @staticmethod
    def generate_terms(x: float, n_terms: int) -> List[float]:
        terms = [x]
        for n in range(1, n_terms):
            terms.append(terms[-1] * (-x ** 2) / ((2 * n) * (2 * n + 1)))
        return terms
