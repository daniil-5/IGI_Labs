import math

class SinSeries:
    """
    Represents a Taylor series approximation of the sine function.
    """

    def __init__(self, x: float, terms: int):
        self.x = x
        self.n = terms

    def evaluate_series(self) -> float:
        result = 0.0
        for i in range(self.n):
            term = ((-1) ** i) * (self.x ** (2 * i + 1)) / math.factorial(2 * i + 1)
            result += term
        return result

    @property
    def math_value(self) -> float:
        return math.sin(self.x)

    def __str__(self):
        return f"sin({self.x}) ≈ {self.evaluate_series()} (n={self.n})"
