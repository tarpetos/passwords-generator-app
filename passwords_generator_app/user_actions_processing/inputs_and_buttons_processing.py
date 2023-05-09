import random
import sqlite3

import pyperclip

from typing import Tuple, List
from customtkinter import CTkEntry, CTkOptionMenu, CTkSlider, CTkSegmentedButton

from ..app_translation.load_data_for_localization import json_localization_data
from ..user_actions_processing.encryption_decryption import encrypt
from ..application_graphical_interface.toplevel_windows import app_loading_screen

from ..user_actions_processing.password_strength_score import (
    strength_rating,
    password_strength,
    make_score_proportion,
    password_strength_chat_gpt,
)

from ..app_translation.messagebox_with_lang_change import (
    invalid_id_input_message,
    id_input_message,
    remake_table_message,
    empty_table_message,
    successful_delete_message,
    successful_remake_table_message,
)

from ..app_translation.messagebox_with_lang_change import (
    nothing_to_copy_message,
    ask_write_to_database_message,
    successful_write_to_database_message,
    ask_if_record_exist_message,
    unexpected_database_error_message,
)

from ..user_actions_processing.main_checks import (
    check_if_description_existing,
    check_password_description_input,
    check_password_result_input,
    check_if_repeatable_characters_is_present,
    check_for_repeatable_characters,
)

from ..database_connections.local_db_connection import PasswordStore


database_user_data = PasswordStore()


def follow_user_if_record_repeats(
        lang_state: str,
        description_store: PasswordStore,
        password_description: Tuple[str]
) -> bool | int:
    if check_if_description_existing(description_store, password_description):
        user_choice = ask_if_record_exist_message(lang_state)
        return user_choice

    return -1


def write_to_database(lang_state: str, password_description: str, result_password: str) -> None:
    if not check_password_description_input(lang_state, password_description):
        return

    if not check_password_result_input(lang_state, result_password):
        return

    user_choice = ask_write_to_database_message(lang_state)

    try:
        if user_choice:
            yes_no_choice = follow_user_if_record_repeats(lang_state, database_user_data, (f'{password_description}',))
            encrypted_password = encrypt(result_password)
            write_data_to_db_conditions(
                lang_state, yes_no_choice, password_description, encrypted_password, result_password
            )
    except sqlite3.OperationalError:
        unexpected_database_error_message(lang_state)


def write_data_to_db_conditions(
        lang_state: str,
        user_choice: bool | int,
        password_description: str,
        encrypted_password: str,
        result_password: str
) -> None:
    if user_choice == -1:
        database_user_data.insert_into_tb(
            password_description,
            encrypted_password,
            len(result_password),
            check_if_repeatable_characters_is_present(result_password)
        )
        successful_write_to_database_message(lang_state)
    elif user_choice:
        database_user_data.update_existing_password(
            encrypted_password,
            len(result_password),
            check_if_repeatable_characters_is_present(result_password),
            password_description
        )
        successful_write_to_database_message(lang_state)


def generate_password(
        lang_state: str,
        pass_usage_entry: CTkEntry,
        pass_length_slider: CTkSlider,
        repeatable_btn: CTkSegmentedButton,
        result_pass_entry: CTkEntry,
        pass_alphabet: str
) -> None:
    pass_usage = pass_usage_entry.get()
    if not check_password_description_input(lang_state, pass_usage):
        return

    pass_length = pass_length_slider.get()
    check_if_repeatable_allowed = repeatable_btn.get()

    result_pass_entry.delete(0, 'end')
    result = check_for_repeatable_characters(lang_state, pass_alphabet, int(pass_length), check_if_repeatable_allowed)
    result_pass_entry.insert(0, result)


def get_menu_option(lang_state: str, chosen_difficulty_option: str) -> int:
    password_random_length_options = {
        json_localization_data[lang_state]['symbols_option_menu'][0]: random.randint(1, 6),
        json_localization_data[lang_state]['symbols_option_menu'][1]: random.randint(3, 6),
        json_localization_data[lang_state]['symbols_option_menu'][2]: random.randint(5, 10),
        json_localization_data[lang_state]['symbols_option_menu'][3]: random.randint(5, 10),
        json_localization_data[lang_state]['symbols_option_menu'][4]: random.randint(15, 20),
        json_localization_data[lang_state]['symbols_option_menu'][5]: random.randint(20, 30),
        json_localization_data[lang_state]['symbols_option_menu'][6]: random.randint(30, 50),
        json_localization_data[lang_state]['symbols_option_menu'][7]: random.randint(50, 100),
    }

    for key in password_random_length_options:
        if key == chosen_difficulty_option:
            return password_random_length_options[key]


def get_password_with_necessary_difficulty(lang_state: str, pass_alphabet: str, expected_result: str) -> str:
    actual_result = None
    generated_pass = None

    while actual_result != expected_result:
        pass_length = get_menu_option(lang_state, expected_result)

        generated_pass = check_for_repeatable_characters(
            lang_state, pass_alphabet, pass_length, json_localization_data[lang_state]['repeatable_segment_btn'][0]
        )

        shannon_pass = password_strength(generated_pass)
        chat_gpt_pass = make_score_proportion(password_strength_chat_gpt(generated_pass))
        average_score = int(round(((shannon_pass + chat_gpt_pass) / 2), 2))

        actual_result = strength_rating(lang_state, average_score)

    return generated_pass


def simple_generate_password(
        lang_state: str,
        result_pass_entry: CTkEntry,
        current_menu_option: CTkOptionMenu,
        description_entry: CTkEntry,
        switch_is_active: bool,
        pass_alphabet: str
):
    result_pass_entry.delete(0, 'end')
    current_menu_option_value = current_menu_option.get()
    result_pass = get_password_with_necessary_difficulty(lang_state, pass_alphabet, current_menu_option_value)
    result_pass_entry.insert(0, result_pass)

    description = description_entry.get()

    if switch_is_active and description:
        database_user_data.insert_update_into_tb(
            description,
            encrypt(result_pass),
            len(result_pass),
            check_if_repeatable_characters_is_present(result_pass)
        )


def copy_password(lang_state: str, result_password_entry: CTkEntry):
    copied_str = result_password_entry.get()
    if copied_str == '':
        nothing_to_copy_message(lang_state)
    else:
        pyperclip.copy(copied_str)


def clear_entries(password_description_entry: CTkEntry, result_password_entry: CTkEntry):
    password_description_entry.delete(0, 'end')
    result_password_entry.delete(0, 'end')


def open_tuples_in_lst() -> List[int]:
    get_all_id = database_user_data.select_id()

    without_tuples_lst = []

    first_tuple_index_value = 0
    for id_value in get_all_id:
        without_tuples_lst.append(id_value[first_tuple_index_value])

    return without_tuples_lst


def remove_record_from_table(lang_state: str) -> None | int:
    if database_user_data.select_full_table().empty:
        empty_table_message(lang_state)
        return

    id_list = open_tuples_in_lst()

    while True:
        chosen_id = id_input_message(lang_state)

        if chosen_id is None:
            return

        try:
            chosen_id = int(chosen_id)

            if chosen_id == -1:
                if remake_table_message(lang_state):
                    load_screen = app_loading_screen(lang_state)
                    database_user_data.drop_table()
                    database_user_data.create_table()
                    load_screen.destroy()
                    successful_remake_table_message(lang_state)
                return 0

            if chosen_id not in id_list:
                invalid_id_input_message(lang_state)
                continue
            else:
                database_user_data.delete_by_id(chosen_id)
                successful_delete_message(lang_state)
                return 0
        except ValueError:
            invalid_id_input_message(lang_state)
