"""
Lab 4

Task 1: Music Applicants Management

Developer: Daniil Maryin
Date: 2025-04-22
"""

from Task1.applicant_list import CsvApplicantList, PickleApplicantList
from Task1.applicant import Applicant


def get_non_empty_input(prompt):
    """Helper function to get non-empty input from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: This field cannot be empty. Please try again.")


def run_applicants_system():
    applicant_list = None
    current_format = None  # 'csv' or 'pickle'

    while True:
        print("\nMain Menu:")
        print("1. Choose data format (CSV/Pickle)")
        print("2. Add applicant")
        print("3. Display exam lists by instrument")
        print("4. Search applicant by surname")
        print("5. Save data")
        print("6. Load data")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            fmt = input("Choose format (csv/pickle): ").lower()

            if fmt not in ('csv', 'pickle'):
                print("Invalid format. Please choose 'csv' or 'pickle'.")
                continue
            current_format = fmt
            print(f"Data format set to {fmt.upper()}.")

        elif choice == '2':
            if current_format is None:
                print("Please choose data format first (Option 1).")
                continue
            try:
                surname = get_non_empty_input("Enter applicant's surname: ")
                instrument = get_non_empty_input("Enter musical instrument: ")
                new_applicant = Applicant(surname, instrument)
                if applicant_list is None:
                    applicant_list = CsvApplicantList() if current_format == 'csv' else PickleApplicantList()
                applicant_list.add_applicant(new_applicant)
                print("Applicant added successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            if not applicant_list or not applicant_list.applicants:
                print("No applicants to display.")
                continue
            applicant_list.sort_by_instrument()
            groups = applicant_list.group_by_instrument()
            for instrument, apps in groups.items():
                print(f"\nExam list for {instrument}:")
                for app in apps:
                    print(f"- {app.surname}")

        elif choice == '4':
            if not applicant_list or not applicant_list.applicants:
                print("No applicants to search.")
                continue
            surname = get_non_empty_input("Enter surname to search: ")
            results = applicant_list.search_by_surname(surname)
            if results:
                print("Matching applicants:")
                for app in results:
                    print(f"- {app}")
            else:
                print("No applicants found with that surname.")

        elif choice == '5':
            if not applicant_list or not applicant_list.applicants:
                print("No data to save.")
                continue
            filename = input("Enter filename: ").strip()
            if not filename:
                print("Error: Filename cannot be empty.")
                continue
            try:
                applicant_list.save(filename)
                print("Data saved successfully.")
            except Exception as e:
                print(f"Error saving data: {e}")

        elif choice == '6':
            if current_format is None:
                print("Please choose data format first (Option 1).")
                continue
            filename = input("Enter filename: ").strip()
            if not filename:
                print("Error: Filename cannot be empty.")
                continue
            try:
                if current_format == 'csv':
                    applicant_list = CsvApplicantList.load(filename)
                else:
                    applicant_list = PickleApplicantList.load(filename)
                print("Data loaded successfully.")
            except Exception as e:
                print(f"Error loading data: {e}")

        elif choice == '7':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1-7.")
