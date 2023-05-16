from string import ascii_letters, digits, punctuation


def exclude_invalid_punctuation_for_markup() -> str:
    excluded_punctuation = '''<>&"'`'''
    allowed_punctuation = ''.join([char for char in punctuation if char not in excluded_punctuation])

    return allowed_punctuation

DEFAULT_LETTERS = ascii_letters
DEFAULT_DIGITS = digits
DEFAULT_PUNCTUATION = exclude_invalid_punctuation_for_markup()
