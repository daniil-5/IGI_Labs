import numpy as np

class MedianCalculator:
    @staticmethod
    def using_numpy(column: np.ndarray):
        return np.median(column)

    @staticmethod
    def manual_median(column: np.ndarray):
        sorted_col = np.sort(column)
        n = len(sorted_col)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_col[mid - 1] + sorted_col[mid]) / 2
        else:
            return sorted_col[mid]