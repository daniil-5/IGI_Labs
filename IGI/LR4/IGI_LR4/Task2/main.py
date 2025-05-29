"""
This program is designed to analyze text files
"""

from Task2.text_analysis import TextAnalyzer
from Task2.file_manager import FileManager


class TextProcessor:
    """Main class for text processing and analysis."""

    def __init__(self, input_file, output_file, zip_name):
        self.input_file = input_file
        self.output_file = output_file
        self.zip_name = zip_name
        self.analyzer = TextAnalyzer()
        self.file_manager = FileManager()

    def run(self):
        """Run the main logic of the text processor."""
        while True:
            try:
                text = self.file_manager.read_file(self.input_file)
                target_length = self.get_valid_len("Enter the word length for replacement: ")
                modified_text = self.analyzer.modify_text(text, target_length)
                report = self.analyzer.generate_report(text, modified_text)
                self.file_manager.save_and_archive(
                    self.output_file, self.zip_name, modified_text, report
                )
                print("Analysis complete. Results saved and archived.")
            except Exception as e:
                print(f"An error occurred: {e}")
            if input("Do you want to analyze another file? (yes/no): ").lower() != "yes":
                print("Goodbye!")
                break

    @staticmethod
    def get_valid_input(prompt, expected_type):
        """Ensure valid user input."""
        while True:
            try:
                return expected_type(input(prompt))
            except ValueError:
                print(f"Invalid input. Please enter a valid {expected_type.__name__}.")

    @staticmethod
    def get_valid_len(prompt):
        """Ensure valid user input."""
        while True:
            try:
                val = int(input(prompt))
                if val >= 3:
                    return val
                else:
                    raise ValueError
            except ValueError:
                print(f"Invalid input. Please enter a valid int number bigger or equal that 3.")

def run_text_analyzing():
    processor = TextProcessor("Task2/input.txt", "Task2/output.txt", "Task2/results.zip")
    processor.run()