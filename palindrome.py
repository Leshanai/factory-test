def is_palindrome(value):
    """Return True if a string or non-negative int reads the same reversed.

    Strings are lowercased and stripped of non-alphanumeric characters first.
    Negative ints are never palindromes. Other types raise TypeError.
    """
    if isinstance(value, str):
        text = "".join(c for c in value.lower() if c.isalnum())
    elif isinstance(value, int) and not isinstance(value, bool):
        if value < 0:
            return False
        text = str(value)
    else:
        raise TypeError(
            f"is_palindrome expects a str or int, got {type(value).__name__}"
        )
    return text == text[::-1]
