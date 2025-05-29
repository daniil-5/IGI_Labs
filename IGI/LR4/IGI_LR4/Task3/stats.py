import statistics
import math

class StatMixin:
    def mean(self):
        return statistics.mean(self.data)

    def median(self):
        return statistics.median(self.data)

    def mode(self):
        try:
            return statistics.mode(self.data)
        except statistics.StatisticsError:
            return "No unique mode"

    def variance(self):
        return statistics.variance(self.data)

    def std_dev(self):
        return statistics.stdev(self.data)

class SeriesStats(StatMixin):
    """
    Encapsulates statistical analysis on a series of values.
    """
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def display_statistics(self):
        print("\n--- Statistics ---")
        print(f"Mean: {self.mean():.6f}")
        print(f"Median: {self.median():.6f}")
        print(f"Mode: {self.mode()}")
        print(f"Variance: {self.variance():.6f}")
        print(f"Standard Deviation: {self.std_dev():.6f}")
