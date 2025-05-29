"""
Module: Text Analysis Utilities
Contains classes and methods for analyzing and modifying text.
"""

import re
from collections import defaultdict


class TextAnalyzer:
    """Class for performing text analysis and modifications."""

    def modify_text(self, text, target_length):
        """
        Modify words of a specific length by replacing the last 3 characters.

        Args:
            text (str): The input text.
            target_length (int): Target word length for modification.

        Returns:
            str: The modified text.
        """
        return re.sub(
            rf'\b\w{{{target_length}}}\b',
            lambda m: m.group()[:-3] + "$" * 3,
            text
        )

    def generate_report(self, original_text, modified_text):
        """
        Generate a detailed report on the text analysis.

        Args:
            original_text (str): The original unmodified text.
            modified_text (str): The modified text.

        Returns:
            str: The analysis report.
        """
        times = self._find_times(original_text)
        words = self._find_words(original_text)
        sentences = self._split_sentences(original_text)

        return "\n".join([
            "=== Analysis Results ===",
            f"1. Found time markers: {len(times)} ({', '.join(times)})",
            f"2. Words of maximum length: {self._max_length_words(words)}",
            f"3. Words before punctuation: {', '.join(self._words_before_punctuation(original_text))}",
            f"4. Longest word ending with 'e': {self._longest_word_ending_e(words)}",
            "\nGeneral Statistics:",
            f"• Sentences: {len(sentences)}",
            f"• By type: {self._sentence_types(sentences)}",
            f"• Average sentence length: {self._average_sentence_length(sentences):.1f}",
            f"• Average word length: {self._average_word_length(words):.1f}",
            f"• Smileys: {self._count_smileys(original_text)}"
        ])

    @staticmethod
    def _find_times(text):
        return re.findall(r'\b(?:[01]\d|2[0-3]):[0-5]\d\b', text)

    @staticmethod
    def _find_words(text):
        return re.findall(r'\b\w+\b', text)

    @staticmethod
    def _split_sentences(text):
        return re.split(r'(?<=[.!?])\s+', text)

    @staticmethod
    def _max_length_words(words):
        lengths = [len(w) for w in words]
        return len([w for w in words if len(w) == max(lengths)])

    @staticmethod
    def _words_before_punctuation(text):
        return re.findall(r'\b\w+\b(?=\s*[,\.])', text)

    @staticmethod
    def _longest_word_ending_e(words):
        e_words = [w for w in words if w.lower().endswith('е')]
        return max(e_words, key=len) if e_words else "None"

    @staticmethod
    def _sentence_types(sentences):
        types = defaultdict(int)
        for s in sentences:
            types['Declarative'] += s.endswith('.')
            types['Interrogative'] += s.endswith('?')
            types['Exclamatory'] += s.endswith('!')
        return ", ".join([f"{k}: {v}" for k, v in types.items()])

    @staticmethod
    def _average_sentence_length(sentences):
        words = [len(re.findall(r'\w+', s)) for s in sentences]
        return sum(words) / len(sentences) if sentences else 0

    @staticmethod
    def _average_word_length(words):
        return sum(len(w) for w in words) / len(words) if words else 0

    @staticmethod
    def _count_smileys(text):
        return len(re.findall(r'[:;]-*([()\[\]])\1*', text))