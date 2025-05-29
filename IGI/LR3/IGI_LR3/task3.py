"""MODULE for counting punctuation marks in text"""

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