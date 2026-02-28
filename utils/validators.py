"""
utils/validators.py
───────────────────
Input validation helpers.
"""

from config.settings import EXIT_KEYWORDS


def detect_exit(text: str) -> bool:
    """
    Return True if the user's message signals intent to end the conversation.

    Strategy:
    - Normalise to lowercase and strip surrounding whitespace.
    - Check if any exit keyword appears as a whole word in the text.
      Using a word-boundary approach avoids false positives like "byebye"
      or "stopped" while still catching "I'm done", "goodbye everyone", etc.

    Parameters
    ----------
    text : str
        Raw user input.

    Returns
    -------
    bool
    """
    normalised = text.lower().strip()

    # Exact match (e.g. user typed just "bye")
    if normalised in EXIT_KEYWORDS:
        return True

    # Whole-word match within a longer sentence
    words = set(normalised.split())
    return bool(words & EXIT_KEYWORDS)
