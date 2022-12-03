import sqlite3
import pyperclip
from string import digits, ascii_letters, punctuation
from tkinter.constants import END
from random import choices, sample

from lists_with_text_for_translation.en_lists_with_transalation import english_list_of_text_for_labels, \
    english_list_of_text_for_buttons, english_list_of_text_for_radiobtns, english_list_of_text_for_table_buttons, \
    english_tuple_of_columns_names
from lists_with_text_for_translation.uk_lists_with_translation import ukrain_list_of_text_for_labels, \
    ukrain_list_of_text_for_radiobtns, ukrain_list_of_text_for_buttons, ukrain_list_of_text_for_table_buttons, \
    ukrain_tuple_of_columns_names
from modules.change_window_config import label_lang_change, change_en_buttons_width, radiobtn_lang_change, \
    btn_lang_change, change_uk_buttons_width
from modules.create_directory_and_txt import create_directory, create_txt
from modules.messagebox_with_lang_change import ivalid_password_usage_message, invalid_password_type_message, \
    invalid_password_value_message, invalid_value_if_no_repeatable_characters_message, \
    invalid_value_for_repeatable_or_not_message
from modules.search_for_description_in_database import check_if_description_existing
from modules.store_user_passwords import StoreUserPasswords
from modules.messagebox_with_lang_change import nothing_to_copy_message, empty_result_input_message, \
    ask_write_to_database_message, successful_write_to_database_message, ask_if_record_exist_message, \
    unexpected_database_error_message, clear_all_fields_message, copy_successful_message

lang_state = True
lang_table_page_state = True
HALF_VARCHAR = 384


def english_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict):
    global lang_state
    lang_state = True

    label_lang_change(labels_dict, english_list_of_text_for_labels)
    btn_lang_change(buttons_dict, english_list_of_text_for_buttons)
    change_en_buttons_width(buttons_dict)
    radiobtn_lang_change(radiobtn_dict, english_list_of_text_for_radiobtns)


def english_language_table_window_data(buttons_dict):
    global lang_table_page_state
    lang_table_page_state = True
    btn_lang_change(buttons_dict, english_list_of_text_for_table_buttons)


def ukrainian_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict):
    global lang_state
    lang_state = False

    label_lang_change(labels_dict, ukrain_list_of_text_for_labels)
    btn_lang_change(buttons_dict, ukrain_list_of_text_for_buttons)
    change_uk_buttons_width(buttons_dict)
    radiobtn_lang_change(radiobtn_dict, ukrain_list_of_text_for_radiobtns)


def ukrainian_language_table_window_data(buttons_dict):
    global lang_table_page_state
    lang_table_page_state = False
    btn_lang_change(buttons_dict, ukrain_list_of_text_for_table_buttons)


def get_data_from_database_table() -> list:
    create_directory()
    create_txt()
    get_list_of_data = StoreUserPasswords()
    full_list_of_data = get_list_of_data.select_full_table()

    full_list_of_data = check_columns_names(full_list_of_data)
    return full_list_of_data


def check_columns_names(full_list_of_data):
    global lang_table_page_state
    if lang_table_page_state:
        full_list_of_data.insert(0, english_tuple_of_columns_names)
        lang_table_page_state = True
    else:
        full_list_of_data.insert(0, ukrain_tuple_of_columns_names)
        lang_table_page_state = False

    return full_list_of_data


def check_for_repeatable_charachters(password_alphabet, password_length, check_if_repeatable_allowed) -> str:
    if check_if_repeatable_allowed.capitalize() == 'Y':
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed.capitalize() == 'N':
        return ''.join(sample(password_alphabet, k=password_length))


def check_if_repeatable_characters_is_present(result_password) -> bool:
    for count_character, character in enumerate(result_password, 1):
        if result_password.count(character) > 1:
            return True
        elif count_character == len(result_password):
            return False


def check_password_usage_input(user_input) -> bool:
    if 0 < len(user_input) <= HALF_VARCHAR:
        return True
    else:
        ivalid_password_usage_message(lang_state)
        return False


def check_password_length_input(user_input) -> bool:
    if not user_input.isdigit():
        invalid_password_type_message(lang_state)
        return False
    elif int(user_input) > HALF_VARCHAR or int(user_input) <= 0:
        invalid_password_value_message(lang_state)
        return False
    else:
        return True


def check_repeatable_input(user_input, password_length_entry, password_length, password_alphabet) -> bool:
    if user_input.capitalize() == 'N' and int(password_length) > len(password_alphabet):
        invalid_value_if_no_repeatable_characters_message(lang_state, password_alphabet)
        password_length_entry.delete(0, END)
        return False
    elif user_input.capitalize() == 'Y' or user_input.capitalize() == 'N':
        return True
    else:
        invalid_value_for_repeatable_or_not_message(lang_state)
        return False


def check_password_result_input(result_password) -> bool:
    if result_password == '':
        empty_result_input_message(lang_state)
        return False
    else:
        return True


def follow_user_if_record_repeats(description_store, password_usage) -> bool or int:
    if check_if_description_existing(description_store, password_usage):
        user_choice = ask_if_record_exist_message(lang_state)
        return user_choice
    else:
        return -1


def write_to_database(password_usage, password_length, result_password):
    if not check_password_usage_input(password_usage):
        return

    if not check_password_length_input(password_length):
        return

    if not check_password_result_input(result_password):
        return

    user_choice = ask_write_to_database_message(lang_state)

    try:
        if user_choice:
            change_data = StoreUserPasswords()
            yes_no_choice = follow_user_if_record_repeats(change_data, (f'{password_usage}',))

            if yes_no_choice == -1:
                change_data.insert_to_tb(
                    password_usage,
                    result_password,
                    password_length,
                    check_if_repeatable_characters_is_present(result_password)
                )
                successful_write_to_database_message(lang_state)
            elif yes_no_choice:
                change_data.update_existing_password(
                    result_password,
                    password_length,
                    check_if_repeatable_characters_is_present(result_password),
                    password_usage
                )
                successful_write_to_database_message(lang_state)
            else:
                pass
        else:
            pass
    except sqlite3.OperationalError:
        unexpected_database_error_message(lang_state)


def get_radiobtn_option(var) -> str:
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


def copy_password(result_password_entry):
    copied_str = result_password_entry.get()
    if copied_str == '':
        nothing_to_copy_message(lang_state)
    else:
        pyperclip.copy(copied_str)
        # copy_successful_message(lang_state) # uncomment this if you want to see a message after a successful copy


def clear_entries(password_usage_entry, password_length_entry, repeatable_entry, result_password_entry):
    password_usage_entry.delete(0, END)
    password_length_entry.delete(0, END)
    repeatable_entry.delete(0, END)
    result_password_entry.delete(0, END)
    # clear_all_fields_message(lang_state) # uncomment this if you want to see a message after clearing the fields
