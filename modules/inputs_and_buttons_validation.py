import sqlite3
import pyperclip
from string import digits, ascii_letters, punctuation
from tkinter.constants import END
from random import choices, sample

from modules.messagebox_with_lang_change import ivalid_password_usage_message, invalid_password_type_message, \
     invalid_password_value_message, invalid_value_if_no_repeatable_characters_message, \
     invalid_value_for_repeatable_or_not_message
from modules.create_directory_and_txt import create_directory, create_txt
from modules.store_user_passwords import StoreUserPasswords
from modules.messagebox_with_lang_change import nothing_to_copy_message, copy_successful_message, \
     ask_write_to_database_message, successful_write_to_database_message, \
     unexpected_database_error_message, clear_all_fields_message

lang_state = True


def label_lang_change(labels_dict, list_of_labels):
    for label_number, label in enumerate(labels_dict):
        labels_dict[label].config(text=list_of_labels[label_number])


def btn_lang_change(buttons_dict, list_of_buttons):
    for btn_number, btn in enumerate(buttons_dict):
        buttons_dict[btn].config(text=list_of_buttons[btn_number])


def radiobtn_lang_change(radiobtns_dict, list_of_radiobtns):
    for btn_number, btn in enumerate(radiobtns_dict):
        radiobtns_dict[btn].config(text=list_of_radiobtns[btn_number])


def english_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict):
    global lang_state
    lang_state = True
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

    english_list_of_text_for_radiobtns = [
        'All symbols',
        'Only letters',
        'Only digits',
        'Letters & digits',
        'Letters & signs',
        'Digits & signs',
    ]

    label_lang_change(labels_dict, english_list_of_text_for_labels)
    btn_lang_change(buttons_dict, english_list_of_text_for_buttons)
    radiobtn_lang_change(radiobtn_dict, english_list_of_text_for_radiobtns)


def ukrainian_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict):
    global lang_state
    lang_state = False
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

    ukrain_list_of_text_for_radiobtns = [
        'Усі символи',
        'Тільки букви',
        'Тільки цифри',
        'Букви і цифри',
        'Букви і знаки',
        'Цифри і знаки',
    ]

    label_lang_change(labels_dict, ukrain_list_of_text_for_labels)
    btn_lang_change(buttons_dict, ukrain_list_of_text_for_buttons)
    radiobtn_lang_change(radiobtn_dict, ukrain_list_of_text_for_radiobtns)


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


def get_radiobtn_option(var):
    if var.get() == 1:
        return digits + ascii_letters + punctuation
    elif var.get() == 2:
        return ascii_letters
    elif var.get() == 3:
        return digits
    elif var.get() == 4:
        return digits + ascii_letters
    elif var.get() == 5:
        return ascii_letters + punctuation
    elif var.get() == 6:
        return digits + punctuation


def generate_password(password_usage_entry, password_length_entry, repeatable_entry, result_password_entry, var):
    password_alphabet = get_radiobtn_option(var)

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
