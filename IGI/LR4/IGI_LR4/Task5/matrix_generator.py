import numpy as np

class MatrixGenerator:
    def __init__(self, rows: int, cols: int, min_val: int = 0, max_val: int = 10):
        self.rows = rows
        self.cols = cols
        self.min_val = min_val
        self.max_val = max_val

    def generate_matrix(self) -> np.ndarray:
        return np.array(list(self._yield_matrix()))

    def _yield_matrix(self):
        for _ in range(self.rows):
            yield [np.random.randint(self.min_val, self.max_val + 1) for _ in range(self.cols)]