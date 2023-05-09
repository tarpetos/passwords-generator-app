from random import choices, sample
from typing import Tuple

from ..app_translation.load_data_for_localization import json_localization_data
from ..app_translation.messagebox_with_lang_change import (
    invalid_password_description_message,
    empty_result_input_message,
)


MAX_PASSWORD_DESCRIPTION_LENGTH = 500


def check_for_repeatable_characters(
        lang_state: str,
        password_alphabet: str,
        password_length: int,
        check_if_repeatable_allowed: str,
) -> str:
    repeatable_allowed_check_value = json_localization_data[lang_state]['repeatable_segment_btn'][0]
    repeatable_not_allowed_check_value = json_localization_data[lang_state]['repeatable_segment_btn'][1]
    if check_if_repeatable_allowed == repeatable_allowed_check_value:
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed == repeatable_not_allowed_check_value:
        return ''.join(sample(password_alphabet, k=password_length))


def check_if_repeatable_characters_is_present(result_password: str) -> bool:
    for count_character, character in enumerate(result_password, 1):
        if result_password.count(character) > 1:
            return True
        elif count_character == len(result_password):
            return False


def check_password_description_input(lang_state: str, user_input: str) -> bool:
    if 0 < len(user_input) <= MAX_PASSWORD_DESCRIPTION_LENGTH:
        return True

    invalid_password_description_message(lang_state)
    return False


def check_password_result_input(lang_state: str, result_password: str) -> bool:
    if result_password == '':
        empty_result_input_message(lang_state)
        return False
    return True


def check_if_description_existing(store_of_user_passwords, password_description: Tuple[str]) -> bool:
    list_of_descriptions = store_of_user_passwords.select_descriptions()

    return password_description in list_of_descriptions
