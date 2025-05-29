"""
Task 3: Taylor Series Approximation for sin(x)
Author: Daniil Maryin
Date: 2025-04-23
"""
from functools import wraps

from Task3.sin_series import SinSeries
from Task3.stats import SeriesStats
from Task3.plotter import plot_sin_series
from Task3.table_printer import print_table

def validate_number_of_terms(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            n = int(input("Enter n number of terms: "))
            if n <= 0:
                raise ValueError("n must be positive")
            return func(n, *args, **kwargs)
        except ValueError as e:
            print(f"Error: {e}")
            return None

    return wrapper

@validate_number_of_terms
def taylor_sin_compute(n_terms):
    x_values = [i * 0.5 for i in range(-12, 13)]  # from -6π to 6π
    # n_terms = 10
    results = []

    for x in x_values:
        sin_obj = SinSeries(x, n_terms)
        approx = sin_obj.evaluate_series()
        real = sin_obj.math_value
        eps = abs(approx - real)

        results.append({
            'x': x,
            'n': n_terms,
            'F(x)': approx,
            'Math F(x)': real,
            'eps': eps
        })

    print_table(results)

    stats = SeriesStats([r['F(x)'] for r in results])
    stats.display_statistics()

    plot_sin_series(x_values, [r['F(x)'] for r in results], [r['Math F(x)'] for r in results])

