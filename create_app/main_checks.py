from random import choices, sample

from app_translation.messagebox_with_lang_change import invalid_password_usage_message, \
    invalid_value_if_no_repeatable_characters_message, \
    invalid_value_for_repeatable_or_not_message, empty_result_input_message


MAX_AUTO_PASSWORD_AND_DESC_LENGTH = 500


def check_for_repeatable_characters(password_alphabet, password_length, check_if_repeatable_allowed) -> str:
    if check_if_repeatable_allowed == 'Yes' or check_if_repeatable_allowed == 'Так':
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed == 'No' or check_if_repeatable_allowed== 'Ні':
        return ''.join(sample(password_alphabet, k=password_length))


def check_if_repeatable_characters_is_present(result_password) -> bool:
    for count_character, character in enumerate(result_password, 1):
        if result_password.count(character) > 1:
            return True
        elif count_character == len(result_password):
            return False


def check_password_usage_input(lang_state, user_input) -> bool:
    if 0 < len(user_input) <= MAX_AUTO_PASSWORD_AND_DESC_LENGTH:
        return True

    invalid_password_usage_message(lang_state)
    return False


def check_repeatable_input(lang_state, user_choice, pass_length, pass_alphabet) -> bool:
    if (user_choice == 'No' or user_choice == 'Ні') and int(pass_length) > len(pass_alphabet):
        invalid_value_if_no_repeatable_characters_message(lang_state, pass_alphabet)
        return True
    elif user_choice == 'Yes' or user_choice== 'No':
        return False
    elif user_choice == 'Так' or user_choice == 'Ні':
        return False
    else:
        invalid_value_for_repeatable_or_not_message(lang_state)
        return True


def check_password_result_input(lang_state, result_password) -> bool:
    if result_password == '':
        empty_result_input_message(lang_state)
        return False
    else:
        return True


def check_if_description_existing(store_of_user_passwords, password_description) -> bool:
    list_of_descriptions = store_of_user_passwords.select_descriptions()

    return password_description in list_of_descriptions
