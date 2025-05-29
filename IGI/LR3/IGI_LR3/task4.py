""" MODULE for analyzing predefined text"""


def analyze_given_text(text: str) -> dict:
    """
    Performs comprehensive text analysis.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with analysis results
    """

    words = text.replace(",", "")
    words = text.replace(".", "").split()

    consonants = "bcdfghjklmnpqrstvwxyz"

    results = {
        'consonant_end_words': sum(1 for word in words if word[-1].lower() in consonants),
        'avg_word_length': round(sum(len(word) for word in words) / len(words)),
        'every_seventh_word': words[6::7]
    }
    results['words_of_avg_length'] = [word for word in words if len(word) == results['avg_word_length']]

    return results