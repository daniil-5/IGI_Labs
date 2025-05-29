""" Module for process list of numbers"""

import random
from typing import List, Tuple, Generator


def get_list_size() -> int:
    """Gets and validates list size from user."""
    while True:
        try:
            size = int(input("Enter list size (positive integer): "))
            if size > 0:
                return size
            print("Size must be positive.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_initialization_method() -> int:
    """Gets list initialization method from user."""
    print("\nChoose initialization method:")
    print("1. Generate random numbers")
    print("2. Enter numbers manually")
    while True:
        try:
            choice = int(input("Enter choice (1 or 2): "))
            if choice in (1, 2):
                return choice
            print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def generate_random_floats(size :int):
    """
    Generates random float numbers one at a time using yield.

    Args:
        size: Number of floats to generate

    Yields:
        Random float between -10 and 10
    """
    for _ in range(size):
        yield random.uniform(-10, 10)

def initialize_with_generator(size: int) -> List[float]:
    """
    Creates a list of random floats using the generator.

    Args:
        size: Length of the list to generate

    Returns:
        List of generated float numbers
    """
    return list(generate_random_floats(size))


def process_float_list(lst: List[float]) -> Tuple[float, float]:
    """
    Processes list of floats.

    Args:
        lst: List to process

    Returns:
        Tuple of (sum of non-negatives, product between min/max abs)
    """
    if not lst:
        raise ValueError("List cannot be empty")

    non_negative_sum = sum(x for x in lst if x >= 0)
    abs_lst = [abs(x) for x in lst]

    min_idx = abs_lst.index(min(abs_lst))
    max_idx = abs_lst.index(max(abs_lst))

    start, end = sorted([min_idx, max_idx])
    product = 1
    for num in lst[start + 1:end]:
        product *= num

    return non_negative_sum, product