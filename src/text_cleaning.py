import re
from typing import List


def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def basic_clean(text: str) -> str:
    """
    Lowercase + remove most punctuation, keep spaces and alphanumerics.
    Good enough for keyword matching.
    """
    if not text:
        return ""
    text = text.lower()
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r"[^a-z0-9#+./ ]+", " ", text)
    text = normalize_whitespace(text)
    return text


def tokenize(text: str) -> List[str]:
    text = basic_clean(text)
    if not text:
        return []
    return text.split()
