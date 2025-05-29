"""MODULE for Processing integer sequence (sum and even count)"""

from typing import Tuple, List

def initialize_with_user_input(size: int) -> List[float]:
    """
    Gets list elements from user input.

    Args:
        size: Number of elements to input

    Returns:
        List of user-provided float numbers
    """
    while True:
        try:
            print(f"Enter {size} numbers separated by spaces:")
            elements = input().split()
            if len(elements) != size:
                raise ValueError(f"Expected {size} numbers")
            return [float(num) for num in elements]
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def process_integer_sequence() -> Tuple[int, int]:
    """
    Processes integer sequence from user input.

    Returns:
        Tuple of (sum of numbers, count of even naturals)
    """
    total_sum = 0
    even_count = 0

    while True:
        try:
            num = int(input("Enter an integer (0 to stop): "))
            if num == 0:
                break
            total_sum += num
            if num > 0 and num % 2 == 0:
                even_count += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return total_sum, even_count