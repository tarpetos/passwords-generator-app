from string import ascii_letters, digits, punctuation


def exclude_invalid_symbols_for_markup() -> str:
    excluded_symbols = '''<>&"'`'''
    allowed_symbols = ''.join([char for char in punctuation if char not in excluded_symbols])

    return allowed_symbols


trimmed_punctuation = exclude_invalid_symbols_for_markup()


def get_password_alphabet(option_value: int) -> str:
    alphabet_options = {
        1: digits + ascii_letters + trimmed_punctuation,
        2: ascii_letters,
        3: digits,
        4: digits + ascii_letters,
        5: ascii_letters + trimmed_punctuation,
        6: digits + trimmed_punctuation,
    }

    return alphabet_options[option_value] if option_value in alphabet_options else alphabet_options[1]


def get_full_alphabet() -> str:
    return digits + ascii_letters + trimmed_punctuation
