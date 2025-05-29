"""
Module: File Management Utilities
Contains classes and methods for handling file read/write and archiving.
"""

import zipfile


class FileManager:
    """Class for managing file operations."""

    @staticmethod
    def read_file(file_path):
        """
        Read the contents of a file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: The file contents.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def save_and_archive(output_file, zip_name, modified_text, report):
        """
        Save analysis results and archive the output file.

        Args:
            output_file (str): Path to the output file.
            zip_name (str): Name of the zip archive.
            modified_text (str): The modified text content.
            report (str): The analysis report.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{modified_text}\n\n{report}")

        with zipfile.ZipFile(zip_name, "w") as zf:
            zf.write(output_file)
            info = zf.getinfo(output_file)
            print(f"File '{info.filename}' ({info.file_size} bytes) added to archive.")