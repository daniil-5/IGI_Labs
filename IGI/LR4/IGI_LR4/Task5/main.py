"""
Task 5: NumPy Array Analysis
Author: Daniil Maryin
Date: 2025-04-24
"""

from Task5.matrix_generator import MatrixGenerator
from Task5.matrix_analyzer import MatrixAnalyzer
from Task5.median_calculator import MedianCalculator

def get_valid_color(prompt):
    from matplotlib.colors import CSS4_COLORS, TABLEAU_COLORS
    while True:
        color = input(prompt).strip().lower()
        if color in CSS4_COLORS or color in TABLEAU_COLORS:
            return color
        print("Invalid color name. Please enter a valid matplotlib color (e.g., 'blue', 'orange', 'cyan').")

def valid_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 2:
                raise ValueError
        except Exception:
            print("Incorrect input! Enter a positive integer value bigger that 2.")
        else:
            return value


def matrix_actions():
    try:
        rows = valid_input("Enter number of rows: ")
        cols = valid_input("Enter number of columns: ")

        generator = MatrixGenerator(cols=cols, rows=rows)
        matrix = generator.generate_matrix()
        print("Generated Matrix:\n", matrix)

        analyzer = MatrixAnalyzer(matrix)

        col_idx, min_sum_col = analyzer.find_column_with_min_sum()
        print(f"\nColumn with min sum (index {col_idx}): {min_sum_col}")

        median_np = MedianCalculator.using_numpy(min_sum_col)
        median_manual = MedianCalculator.manual_median(min_sum_col)
        print(f"\nMedian (NumPy): {median_np:.2f}")
        print(f"Median (Manual): {median_manual:.2f}")

        print("\nMean of matrix:", analyzer.mean())
        print("Variance:", analyzer.variance())
        print("Standard Deviation:", analyzer.std_deviation())
        print("Correlation Coefficient Matrix:\n", analyzer.correlation_matrix())

    except ValueError as ve:
        print("Error:", ve)

if __name__ == "__main__":
    matrix_actions()
