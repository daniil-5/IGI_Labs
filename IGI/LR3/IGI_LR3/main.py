from typing import List, Tuple
from task1 import compute_and_compare_sin
from task2 import initialize_with_user_input, process_integer_sequence
from task3 import count_punctuation_marks
from task4 import analyze_given_text
from task5 import get_list_size, get_initialization_method, initialize_with_generator, process_float_list

"""
Lab Work #3
Version: 2.0
Author: Марьин Даниил
Date: [26/03/2025]
"""

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