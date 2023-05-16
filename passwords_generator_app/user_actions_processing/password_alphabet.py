from .default_alphabet import DEFAULT_LETTERS, DEFAULT_DIGITS, DEFAULT_PUNCTUATION
from ..database_connections.alphabet_store import AlphabetStore

alphabet_db_connector = AlphabetStore()


class PasswordAlphabet:
    def __init__(self):
        self._default_letters = DEFAULT_LETTERS
        self._default_digits = DEFAULT_DIGITS
        self._default_punctuation = DEFAULT_PUNCTUATION

        self.custom_letters = None
        self.custom_digits = None
        self.custom_punctuation = None

    def check_custom_alphabet_for_existence(self):
        alphabet_data = alphabet_db_connector.select_alphabet()

        if alphabet_data is not None:
            self.custom_letters = alphabet_data[1]
            self.custom_digits = alphabet_data[2]
            self.custom_punctuation = alphabet_data[3]
        else:
            self.custom_letters = self._default_letters
            self.custom_digits = self._default_digits
            self.custom_punctuation = self._default_punctuation

    def get_password_alphabet(self, option_value: int) -> str:
        self.check_custom_alphabet_for_existence()
        alphabet_options = {
            1: self.custom_letters + self.custom_digits + self.custom_punctuation,
            2: self.custom_letters,
            3: self.custom_digits,
            4: self.custom_letters + self.custom_digits,
            5: self.custom_letters + self.custom_punctuation,
            6: self.custom_digits + self.custom_punctuation,
        }

        return alphabet_options[option_value] if option_value in alphabet_options else alphabet_options[1]

    def get_full_alphabet(self) -> str:
        self.check_custom_alphabet_for_existence()
        return self.custom_letters + self.custom_digits + self.custom_punctuation
