from string import ascii_letters, digits, punctuation

NOT_ALLOWED_PUNCTUATION = '''<>&"'`'''


def exclude_invalid_punctuation_for_markup() -> str:
    allowed_punctuation = ''.join([char for char in punctuation if char not in NOT_ALLOWED_PUNCTUATION])
    return allowed_punctuation


DEFAULT_LETTERS = ascii_letters
DEFAULT_DIGITS = digits
DEFAULT_PUNCTUATION = exclude_invalid_punctuation_for_markup()
