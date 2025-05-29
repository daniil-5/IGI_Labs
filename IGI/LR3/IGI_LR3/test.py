import math
from typing import List, Tuple
from functools import wraps

"""
Lab Work #3
Version: 2.0
Author: Марьин Даниил
Date: [26/03/2025]
"""


def initialize_with_generator(size: int) -> List[float]:
    """
    Generates a list of random float numbers.

    Args:
        size: Length of the list to generate

    Returns:
        List of generated float numbers
    """
    import random
    return [random.uniform(-10, 10) for _ in range(size)]


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


def taylor_sin(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int]:
    """
    Computes sine using Taylor series expansion.

    Args:
        x: Input value in radians
        eps: Required precision
        max_iter: Maximum iterations allowed

    Returns:
        Tuple of (approximate sine value, terms used)
    """
    term = x  # First term
    sum_sin = term
    n = 1

    while abs(term) > eps and n < max_iter:
        term *= -x ** 2 / ((2 * n) * (2 * n + 1))
        sum_sin += term
        n += 1

    return sum_sin, n


def validate_input(func):
    """
    Decorator to validate function inputs.
    Ensures positive epsilon and handles value errors.
    """

    @wraps(func) # Saves the metadata of the function
    def wrapper(*args, **kwargs):
        try:
            x = float(input("Enter x (in radians): "))
            eps = float(input("Enter precision (epsilon): "))
            if eps <= 0:
                raise ValueError("Epsilon must be positive.")
            return func(x, eps, *args, **kwargs)
        except ValueError as e:
            print(f"Invalid input: {e}")
            return None

    return wrapper


@validate_input
def compute_and_compare_sin(x: float, eps: float):
    """
    Computes and compares Taylor series approximation with math.sin

    Args:
        x: Input value in radians
        eps: Required precision
    """
    approx_sin, terms = taylor_sin(x, eps)
    exact_sin = math.sin(x)

    print("\n|    x    |   n   |    F(x)   | Math F(x) |    eps    |")
    print("-" * 50)
    print(f"| {x:^6.3f} | {terms:^5} | {approx_sin:^9.6f} | {exact_sin:^9.6f} | {eps:^9.1e} |")


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


def count_punctuation_marks(text: str) -> int:
    """
    Counts punctuation marks in text.

    Args:
        text: String to analyze

    Returns:
        Count of punctuation marks
    """
    punctuation = """!"'(),-–.:;?{}"""
    return sum(1 for char in text if char in punctuation)


def analyze_given_text(text: str) -> dict:
    """
    Performs comprehensive text analysis.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with analysis results
    """
    words = text.replace(",", "").split()
    consonants = "bcdfghjklmnpqrstvwxyz"

    results = {
        'consonant_end_words': sum(1 for word in words if word[-1].lower() in consonants),
        'avg_word_length': round(sum(len(word) for word in words) / len(words)),
        'every_seventh_word': words[6::7]
    }
    results['words_of_avg_length'] = [word for word in words if len(word) == results['avg_word_length']]

    return results


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


def display_menu():
    """Displays the main program menu."""
    print("\n" + "=" * 50)
    print("MAIN MENU".center(50))
    print("=" * 50)
    print("1. Compute Taylor Series Approximation for sin(x)")
    print("2. Process integer sequence (sum and even count)")
    print("3. Count punctuation marks in text")
    print("4. Analyze predefined text")
    print("5. Process list of numbers")
    print("6. Exit")
    print("=" * 50)


def get_menu_choice() -> int:
    """Gets and validates user menu choice."""
    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")


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


def main() -> None:
    """Main program execution loop."""
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == 1:
            result = compute_and_compare_sin()
            if result is None:
                continue

        elif choice == 2:
            total, evens = process_integer_sequence()
            print(f"\nTotal sum: {total}")
            print(f"Count of even natural numbers: {evens}")

        elif choice == 3:
            text = input("Enter text to analyze: ")
            count = count_punctuation_marks(text)
            print(f"\nNumber of punctuation marks: {count}")

        elif choice == 4:
            sample_text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
            analysis = analyze_given_text(sample_text)

            print("\nText analysis results:")
            print(f"Words ending with consonant: {analysis['consonant_end_words']}")
            print(f"Average word length: {analysis['avg_word_length']}")
            print(f"Words with average length: {', '.join(analysis['words_of_avg_length'])}")
            print(f"Every seventh word: {', '.join(analysis['every_seventh_word'])}")

        elif choice == 5:
            size = get_list_size()
            init_method = get_initialization_method()

            if init_method == 1:
                numbers = initialize_with_generator(size)
            else:
                numbers = initialize_with_user_input(size)

            print("\nGenerated list:", numbers)

            try:
                sum_nn, product = process_float_list(numbers)
                print(f"Sum of non-negative elements: {sum_nn}")
                print(f"Product between min/max absolute: {product}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 6:
            print("\nExiting program. Goodbye!")
            break

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()