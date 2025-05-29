import csv
import pickle

from Task1.applicant import Applicant


class DisplayMixin:
    """Mixin class to add display functionality."""

    def display_applicants(self):
        """Displays all applicants in the list."""
        if not self.applicants:
            print("No applicants to display.")
            return
        for idx, app in enumerate(self.applicants, 1):
            print(f"{idx}. {app}")


class BaseApplicantList(DisplayMixin):
    """Base class for managing a list of applicants."""

    def __init__(self):
        self.applicants = []

    def add_applicant(self, applicant):
        """Adds an applicant to the list."""
        if not isinstance(applicant, Applicant):
            raise TypeError("Can only add Applicant instances.")
        self.applicants.append(applicant)

    def search_by_surname(self, surname):
        """Searches applicants by surname (case-insensitive)."""
        return [app for app in self.applicants if app.surname.lower() == surname.lower()]

    def sort_by_instrument(self):
        """Sorts applicants by instrument and surname."""
        self.applicants.sort(key=lambda x: (x.instrument, x.surname))

    def group_by_instrument(self):
        """Groups applicants by their instrument."""
        groups = {}
        for app in self.applicants:
            if app.instrument not in groups:
                groups[app.instrument] = []
            groups[app.instrument].append(app)
        return groups


class CsvApplicantList(BaseApplicantList):
    """Handles saving and loading applicants to/from CSV files."""

    def save(self, filename):
        """Saves applicants to a CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Surname", "Instrument"])
            for app in self.applicants:
                writer.writerow([app.surname, app.instrument])

    @classmethod
    def load(cls, filename):
        """Loads applicants from a CSV file."""
        instance = cls()
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    surname = row['Surname']
                    instrument = row['Instrument']
                    instance.add_applicant(Applicant(surname, instrument))
        except FileNotFoundError:
            print(f"Warning: File {filename} not found. Starting with empty list.")
        return instance


class PickleApplicantList(BaseApplicantList):
    """Handles saving and loading applicants to/from pickle files."""

    def save(self, filename):
        """Saves applicants to a pickle file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.applicants, f)

    @classmethod
    def load(cls, filename):
        """Loads applicants from a pickle file."""
        instance = cls()
        try:
            with open(filename, 'rb') as f:
                instance.applicants = pickle.load(f)
        except (FileNotFoundError, EOFError):
            print(f"Warning: File {filename} not found or empty. Starting with empty list.")
        return instance