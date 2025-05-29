"""
Allows user to choose between two laboratory works.

Developer: Daniil Maryin
Date: 2025-04-22
"""

import sys
from Task1.main import run_applicants_system
from Task2.main import run_text_analyzing
from Task3.main import taylor_sin_compute
from Task4.main import draw_triangle
from Task5.main import matrix_actions
from External.main import dataset_analizer


def show_main_menu():
    """Display main menu with lab choices."""
    print("\n=== Main Menu ===")
    print("1. Task 1: Applicants Management System")
    print("2. Task 2: Text Analysis System")
    print("3. Task 3: Taylor Series Approximation for sin(x)")
    print("4. Task 4: Draw Triangle")
    print("5. Task 5: NumPy Array Analysis")
    print("6. External: Dataset analyzer")
    print("7. Exit")


def get_choice():
    """Get and validate user choice."""
    while True:
        try:
            choice = int(input("\nChoose laboratory work (1-7): "))
            if 1 <= choice <= 7:
                return choice
            print("Invalid choice. Please enter 1-7.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Main program loop."""
    while True:
        show_main_menu()
        choice = get_choice()

        if choice == 1:
            print("\n=== Applicants Management ===")
            run_applicants_system()

        elif choice == 2:
            print("\n=== Text Analysis ===")
            run_text_analyzing()

        elif choice == 3:
            print("\n=== Taylor Series Approximation for sin(x) ===")
            taylor_sin_compute()

        elif choice == 4:
            print("\n=== Draw Triangle ===")
            draw_triangle()

        elif choice == 5:
            print("\n=== Matrix manipulations ===")
            matrix_actions()

        elif choice == 6:
            print("\n=== External: Dataset analyzer ===")
            dataset_analizer()

        elif choice == 7:
            print("Exiting program. Goodbye!")
            sys.exit()


if __name__ == "__main__":
    main()