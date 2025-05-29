import numpy as np

class MatrixAnalyzer:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix

    def column_sums(self):
        return self.matrix.sum(axis=0)

    def find_column_with_min_sum(self):
        sums = self.column_sums()
        return np.argmin(sums), self.matrix[:,np.argmin(sums)]

    def mean(self):
        return np.mean(self.matrix)

    def variance(self):
        return np.var(self.matrix)

    def std_deviation(self):
        return np.std(self.matrix)

    def correlation_matrix(self):
        return np.corrcoef(self.matrix.T)
