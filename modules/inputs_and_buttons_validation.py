import sqlite3
import pyperclip
from string import digits, ascii_letters, punctuation
from tkinter.constants import END
from random import choices, sample

from modules.messagebox_with_lang_change import ivalid_password_usage_message, invalid_password_type_message, \
    invalid_password_value_message, \
    invalid_value_if_no_repeatable_characters_message, \
    invalid_value_for_repeatable_or_not_message
from modules.create_directory_and_txt import create_directory, create_txt
from modules.store_user_passwords import StoreUserPasswords
from modules.messagebox_with_lang_change import nothing_to_copy_message, copy_successful_message, \
     ask_write_to_database_message, successful_write_to_database_message, \
     unexpected_database_error_message, clear_all_fields_message


lang_state = True


def english_language_main_window_data(labels_dict, buttons_dict):
    global lang_state
    english_list_of_text_for_labels = [
        'For what this password should be?:',
        'Enter password length:',
        'Can be repeatable characters in password(y/n)?:',
        'GENERATED PASSWORD',
    ]

    english_list_of_text_for_buttons = [
        'Generate',
        'Quit',
        'Copy password',
        'Clear all',
    ]

    main_wind_lang_change(labels_dict, buttons_dict, english_list_of_text_for_labels,
                          english_list_of_text_for_buttons)
    lang_state = True


def ukrainian_language_main_window_data(labels_dict, buttons_dict):
    global lang_state
    ukrain_list_of_text_for_labels = [
        'Яке призначення цього пароля?:',
        'Введіть, якої довжини має бути пароль:',
        'Чи можуть бути повторювані символи в паролі(y/n)?:',
        'ЗГЕНЕРОВАНИЙ ПАРОЛЬ',
    ]

    ukrain_list_of_text_for_buttons = [
        'Згенерувати пароль',
        'Вихід з програми',
        'Скопіювати пароль',
        'Очистити всі поля',
    ]

    main_wind_lang_change(labels_dict, buttons_dict, ukrain_list_of_text_for_labels,
                          ukrain_list_of_text_for_buttons)

    lang_state = False


def check_for_repeatable_charachters(password_alphabet, password_length, check_if_repeatable_allowed):
    if check_if_repeatable_allowed.capitalize() == 'Y':
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed.capitalize() == 'N':
        return ''.join(sample(password_alphabet, k=password_length))


def check_if_repeatable_characters_is_present(result_password):
    for character in result_password:
        if result_password.count(character) > 1:
            return True
        else:
            pass

        return False


def check_password_usage_input(user_input):
    if 0 < len(user_input) <= 384:
        return True
    else:
        ivalid_password_usage_message(lang_state)
        return False


def check_password_length_input(user_input):
    if not user_input.isdigit():
        invalid_password_type_message(lang_state)
        return False
    elif int(user_input) > 384 or int(user_input) <= 0:
        invalid_password_value_message(lang_state)
        return False
    else:
        return True


def check_repeatable_input(user_input, password_length_entry, password_length, password_alphabet):
    if user_input.capitalize() == 'N' and int(password_length) > len(password_alphabet):
        invalid_value_if_no_repeatable_characters_message(lang_state, password_alphabet)
        password_length_entry.delete(0, END)
        return False
    elif user_input.capitalize() == 'Y' or user_input.capitalize() == 'N':
        return True
    else:
        invalid_value_for_repeatable_or_not_message(lang_state)
        return False


def write_to_database(password_usage, result_password, password_length):
    user_choice = ask_write_to_database_message(lang_state)

    try:
        if user_choice:
            create_directory()
            create_txt()

            write_data = StoreUserPasswords()
            write_data.insert_to_tb(
                password_usage,
                result_password,
                password_length,
                check_if_repeatable_characters_is_present(result_password)
            )
            successful_write_to_database_message(lang_state)
        else:
            pass
    except sqlite3.OperationalError:
        unexpected_database_error_message(lang_state)


def generate_password(password_usage_entry, password_length_entry, repeatable_entry, result_password_entry):
    password_alphabet = digits + ascii_letters + punctuation

    password_usage = password_usage_entry.get()
    if not check_password_usage_input(password_usage):
        return

    password_length = password_length_entry.get()
    if not check_password_length_input(password_length):
        return

    check_if_repeatable_allowed = repeatable_entry.get()
    if not check_repeatable_input(
            check_if_repeatable_allowed,
            password_length_entry,
            password_length,
            password_alphabet
    ):
        return

    result_password_entry.delete(0, END)
    result = check_for_repeatable_charachters(password_alphabet, int(password_length), check_if_repeatable_allowed)
    result_password_entry.insert(0, result)

    write_to_database(password_usage, result, password_length)


def copy_password(result_password_entry):
    copied_str = result_password_entry.get()
    if copied_str == '':
        nothing_to_copy_message(lang_state)
    else:
        pyperclip.copy(copied_str)
        copy_successful_message(lang_state)


def clear_entries(password_usage_entry, password_length_entry, repeatable_entry, result_password_entry):
    password_usage_entry.delete(0, END)
    password_length_entry.delete(0, END)
    repeatable_entry.delete(0, END)
    result_password_entry.delete(0, END)

    clear_all_fields_message(lang_state)
