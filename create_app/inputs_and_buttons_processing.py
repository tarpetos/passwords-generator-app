import random
import re
import sqlite3
import mysql.connector
import pyperclip
import requests

from random import choices, sample
from string import digits, ascii_letters, punctuation
from typing import Any, Iterator
from pandas import DataFrame

from additional_modules.encryption_decryption import encrypt, decrypt
from additional_modules.password_strength_score import strength_rating, password_strength, make_score_proportion, \
    password_strength_chat_gpt
from additional_modules.toplevel_windows import app_loading_screen, search_screen, password_strength_screen
from app_translation.load_data_for_localization import all_json_localization_data
from app_translation.messagebox_with_lang_change import invalid_password_usage_message, invalid_password_type_message, \
    invalid_password_value_message, invalid_value_if_no_repeatable_characters_message, input_dialog_error_message, \
    invalid_value_for_repeatable_or_not_message, input_dialog_message, ask_to_update_record_message, \
    duplicate_usage_error_message, no_update_warning_message, successful_update_message, ask_to_sync_message, \
    successful_sync_message, error_sync_message, connection_error_message, connection_timeout_message, \
    token_input_message, input_token_error_message, data_is_identical_message, ask_to_save_token_message, \
    choose_between_duplicates_message, show_warn_by_regex_message, server_token_changed_message, remake_table_message, \
    empty_table_warn, ask_to_save_new_token, successfully_changed_token_message, was_not_changed_token_message, \
    search_query_input_message, invalid_search_query_message, \
    no_matches_for_search_message, successful_delete_message, successful_remake_table_message
from app_translation.messagebox_with_lang_change import nothing_to_copy_message, empty_result_input_message, \
    ask_write_to_database_message, successful_write_to_database_message, ask_if_record_exist_message, \
    unexpected_database_error_message
from create_app.store_user_passwords import PasswordStore
from create_app.sync_table import RemoteDB

MAX_AUTO_PASSWORD_AND_DESC_LENGTH = 384
# MAX_PASSWORD_LENGTH_WITHOUT_REPETITIVE = 90

database_user_data = PasswordStore()


def table_column_names() -> tuple[list, list]:
    en_table_columns_names = [column for column in all_json_localization_data['EN']['table_column_names'].values()]
    uk_table_columns_names = [column for column in all_json_localization_data['UA']['table_column_names'].values()]

    return en_table_columns_names, uk_table_columns_names


def retrieve_data_for_build_table_interface(
        lang_state, column_number=5, user_query=None) -> dict[str, list | Iterator[DataFrame] | DataFrame | Any]:
    column_name_localization = table_column_names()
    en_table_lst = column_name_localization[0][:column_number]
    uk_table_lst = column_name_localization[1][:column_number]

    if user_query:
        full_list_of_data = database_user_data.select_search_data_by_desc(user_query)
    else:
        full_list_of_data = database_user_data.select_full_table()

    return {'lang': lang_state, 'english_lst': en_table_lst, 'ukrainian_lst': uk_table_lst, 'data': full_list_of_data}


def check_for_repeatable_characters(password_alphabet, password_length, check_if_repeatable_allowed) -> str:
    if check_if_repeatable_allowed.capitalize() == 'Y' or check_if_repeatable_allowed.capitalize() == 'Т':
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed.capitalize() == 'N' or check_if_repeatable_allowed.capitalize() == 'Н':
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


def check_password_length_input(lang_state, user_input) -> bool:
    if not user_input.isdigit():
        invalid_password_type_message(lang_state)
        return False
    elif int(user_input) > MAX_AUTO_PASSWORD_AND_DESC_LENGTH or int(user_input) <= 0:
        invalid_password_value_message(lang_state)
        return False
    return True


def check_repeatable_input(lang_state, user_input, pass_length_entry, pass_length, pass_alphabet) -> bool:
    if (user_input.capitalize() == 'N' or user_input.capitalize() == 'Н') and int(pass_length) > len(pass_alphabet):
        invalid_value_if_no_repeatable_characters_message(lang_state, pass_alphabet)
        pass_length_entry.delete(0, 'end')
        return True
    elif user_input.capitalize() == 'Y' or user_input.capitalize() == 'N':
        return False
    elif user_input.capitalize() == 'Т' or user_input.capitalize() == 'Н':
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


def check_if_description_existing(store_of_user_passwords, password_description):
    list_of_descriptions = store_of_user_passwords.select_descriptions()

    if password_description in list_of_descriptions:
        return True
    else:
        return False


def follow_user_if_record_repeats(lang_state, description_store, password_usage) -> bool | int:
    if check_if_description_existing(description_store, password_usage):
        user_choice = ask_if_record_exist_message(lang_state)
        return user_choice

    return -1


def write_to_database(lang_state, password_usage, result_password):
    if not check_password_usage_input(lang_state, password_usage):
        return

    if not check_password_result_input(lang_state, result_password):
        return

    user_choice = ask_write_to_database_message(lang_state)

    try:
        if user_choice:
            yes_no_choice = follow_user_if_record_repeats(lang_state, database_user_data, (f'{password_usage}',))
            encrypted_password = encrypt(result_password)
            write_data_to_db_conditions(lang_state, yes_no_choice, password_usage, encrypted_password, result_password)

    except sqlite3.OperationalError:
        unexpected_database_error_message(lang_state)


def write_data_to_db_conditions(lang_state, user_choice, password_usage, encrypted_password, result_password):
    if user_choice == -1:
        database_user_data.insert_into_tb(
            password_usage,
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
            password_usage
        )
        successful_write_to_database_message(lang_state)


def exclude_invalid_symbols_for_markup() -> str:
    excluded_symbols = '<>&"'
    allowed_symbols = ''.join([char for char in punctuation if char not in excluded_symbols])

    return allowed_symbols


def get_radiobtn_option(var) -> str:
    fixed_punctuation = exclude_invalid_symbols_for_markup()

    if var.get() == 1:
        return digits + ascii_letters + fixed_punctuation
    elif var.get() == 2:
        return ascii_letters
    elif var.get() == 3:
        return digits
    elif var.get() == 4:
        return digits + ascii_letters
    elif var.get() == 5:
        return ascii_letters + fixed_punctuation
    elif var.get() == 6:
        return digits + fixed_punctuation


def generate_password(lang_state, pass_usage_entry, pass_length_entry, repeatable_entry, result_pass_entry, var):
    pass_alphabet = get_radiobtn_option(var)

    pass_usage = pass_usage_entry.get()
    if not check_password_usage_input(lang_state, pass_usage):
        return

    pass_length = pass_length_entry.get()
    if not check_password_length_input(lang_state, pass_length):
        return

    check_if_repeatable_allowed = repeatable_entry.get()
    if check_repeatable_input(lang_state, check_if_repeatable_allowed, pass_length_entry, pass_length, pass_alphabet):
        return

    result_pass_entry.delete(0, 'end')
    result = check_for_repeatable_characters(pass_alphabet, int(pass_length), check_if_repeatable_allowed)
    result_pass_entry.insert(0, result)


def get_menu_option(var):
    if var == 'Extremely unreliable':
        return random.randint(1, 6)
    elif var == 'Very easy':
        return random.randint(3, 6)
    elif var == 'Easy':
        return random.randint(5, 10)
    elif var == 'Below average':
        return random.randint(5, 10)
    elif var == 'Average':
        return random.randint(15, 20)
    elif var == 'Strong':
        return random.randint(20, 30)
    elif var == 'Very strong':
        return random.randint(30, 50)
    else:
        return random.randint(50, 100)


def get_password_with_necessary_difficulty(expected_result):
    fixed_punctuation = exclude_invalid_symbols_for_markup()
    pass_alphabet = digits + ascii_letters + fixed_punctuation

    actual_result = None
    generated_pass = None

    count = 0
    while actual_result != expected_result:
        pass_length = get_menu_option(expected_result)

        generated_pass = check_for_repeatable_characters(pass_alphabet, pass_length, 'Y')
        shannon_pass = password_strength(generated_pass)
        chat_gpt_pass = make_score_proportion(password_strength_chat_gpt(generated_pass))
        average_score = round(((shannon_pass + chat_gpt_pass) / 2), 2)

        actual_result = strength_rating(True, average_score)
        count += 1

    print(count)

    return generated_pass


def simple_generate_password(result_pass_entry, current_menu_option, description_entry, switch_is_active):
    result_pass_entry.delete(0, 'end')
    result_pass = get_password_with_necessary_difficulty(current_menu_option)
    result_pass_entry.insert(0, result_pass)

    description = description_entry.get()

    if switch_is_active and description:
        database_user_data.insert_update_into_tb(
            description,
            encrypt(result_pass),
            len(result_pass),
            check_if_repeatable_characters_is_present(result_pass)
        )


def copy_password(lang_state, result_password_entry):
    copied_str = result_password_entry.get()
    if copied_str == '':
        nothing_to_copy_message(lang_state)
    else:
        pyperclip.copy(copied_str)
        # copy_successful_message(lang_state) # uncomment this if you want to see a message after a successful copy


def clear_entries(password_usage_entry, password_length_entry, repeatable_entry, result_password_entry):
    password_usage_entry.delete(0, 'end')
    password_length_entry.delete(0, 'end')
    repeatable_entry.delete(0, 'end')
    result_password_entry.delete(0, 'end')
    # clear_all_fields_message(lang_state) # uncomment this if you want to see a message after clearing the fields


def open_tuples_in_lst() -> list:
    get_all_id = database_user_data.select_id()

    without_tuples_lst = []

    first_tuple_index_value = 0
    for id_value in get_all_id:
        without_tuples_lst.append(id_value[first_tuple_index_value])

    return without_tuples_lst


def remove_record_from_table(lang_state, application_window):
    if database_user_data.select_full_table() is None:
        empty_table_warn(lang_state)
        return

    id_list = open_tuples_in_lst()
    chosen_id = input_dialog_message(lang_state, application_window)

    if chosen_id == -1:
        if remake_table_message(lang_state):
            database_user_data.drop_table()
            database_user_data.create_table()
            successful_remake_table_message(lang_state)
        return

    while True:
        if not chosen_id:
            return

        if chosen_id not in id_list:
            input_dialog_error_message(lang_state)
            chosen_id = input_dialog_message(lang_state, application_window)
        else:
            database_user_data.delete_by_id(chosen_id)
            successful_delete_message(lang_state)
            return 0


def update_record_in_table(lang_state) -> bool:
    return ask_to_update_record_message(lang_state)


def duplicate_usage_in_table(lang_state):
    duplicate_usage_error_message(lang_state)


def nothing_to_update_in_table(lang_state):
    no_update_warning_message(lang_state)


def successful_update_in_table(lang_state):
    successful_update_message(lang_state)


def sync_db_data(lang_state, application_window):
    remote_connection = result_of_connection(lang_state)
    if remote_connection is None:
        return

    ask_to_sync = ask_to_sync_message(lang_state)

    if ask_to_sync:
        full_list_of_tokens = remote_connection.select_all_tokens()
        saved_data = database_user_data.select_from_save_tb()

        user_token = check_for_token(lang_state, application_window, saved_data)
        user_id = check_for_id(remote_connection, saved_data, user_token)

        if user_token is None:
            return

        while True:
            if user_token in full_list_of_tokens:
                user_id = check_for_id(remote_connection, saved_data, user_token)
                save_token(lang_state, saved_data, user_id, user_token, full_list_of_tokens)

                table_name = f'pass_gen_table_{user_id}'
                local_full_table = database_user_data.select_without_id()
                remote_full_table = remote_connection.select_pass_gen_table_without_id(table_name)

                lst_union = set(local_full_table) | set(remote_full_table)

                sorted_united_lst = sorted(lst_union)
                sorted_local_table = sorted(local_full_table)
                sorted_remote_table = sorted(remote_full_table)

                if sorted_local_table == sorted_united_lst and sorted_remote_table == sorted_united_lst:
                    data_is_identical_message(lang_state)
                    return

                temp_lst = local_full_table + remote_full_table
                if check_if_has_duplicates_desc(temp_lst):
                    while True:
                        save_pass = choose_between_duplicates_message(lang_state, application_window)

                        if save_pass == '' or save_pass:
                            local_choice_pattern = re.compile('^(local|локально)$', re.IGNORECASE)
                            remote_choice_pattern = re.compile('^(remote|сервер)$', re.IGNORECASE)
                            if re.match(local_choice_pattern, save_pass):
                                load_screen = app_loading_screen(lang_state)
                                local_full_table = correct_lst_unite(local_full_table, remote_full_table)
                                sync_tables_loop(remote_connection, table_name, local_full_table)
                                load_screen.destroy()
                                successful_sync_message(lang_state)
                                return
                            elif re.match(remote_choice_pattern, save_pass):
                                load_screen = app_loading_screen(lang_state)
                                remote_full_table = correct_lst_unite(remote_full_table, local_full_table)
                                sync_tables_loop(remote_connection, table_name, remote_full_table)
                                load_screen.destroy()
                                successful_sync_message(lang_state)
                                return
                            else:
                                load_screen = app_loading_screen(lang_state)
                                load_screen.destroy()
                                show_warn_by_regex_message(lang_state)
                        else:
                            return
                else:
                    load_screen = app_loading_screen(lang_state)
                    sync_tables_loop(remote_connection, table_name, temp_lst)
                    load_screen.destroy()
                    successful_sync_message(lang_state)
                    return
            else:
                if saved_data:
                    server_token_changed_message(lang_state)
                    database_user_data.truncate_saved_token()
                    user_token = token_input_message(lang_state, application_window)
                    save_token(lang_state, saved_data, user_id, user_token, full_list_of_tokens)
                else:
                    input_token_error_message(lang_state)
                    user_token = token_input_message(lang_state, application_window)

                if user_token is None:
                    return


def result_of_connection(lang_state) -> RemoteDB | None:
    load_screen = app_loading_screen(lang_state)
    remote_connection = control_mysql_connection(lang_state, load_screen)
    if remote_connection == 'MySQL connection error':
        return

    if not check_internet_connection():
        connection_error_message(lang_state, load_screen)
        return

    load_screen.destroy()

    return remote_connection


def update_columns_via_app_interface(lang_state, all_data_from_table):
    all_data_from_table.update_data_using_table_interface(lang_state)


def control_mysql_connection(lang_state, load_screen) -> RemoteDB | str:
    try:
        remote_mysql_obj = RemoteDB()
        return remote_mysql_obj
    except mysql.connector.errors.OperationalError:
        connection_timeout_message(lang_state, load_screen)
        return 'MySQL connection error'
    except mysql.connector.errors.DatabaseError:
        error_sync_message(lang_state, load_screen)
        return 'MySQL connection error'
    except mysql.connector.errors.InterfaceError:
        error_sync_message(lang_state, load_screen)
        return 'MySQL connection error'


def check_internet_connection():
    try:
        requests.get('http://google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False


def check_for_token(lang_state, app, saved_token):
    if saved_token:
        user_token = decrypt(saved_token[1])
    else:
        user_token = token_input_message(lang_state, app)

    return user_token


def check_for_id(remote_connection, saved_token, user_token):
    if saved_token:
        user_id = decrypt(saved_token[0])
    else:
        user_id = remote_connection.select_id_by_token(encrypt(user_token))

    return user_id


def save_token(lang_state, token_to_save, user_id, user_token, full_list_of_tokens):
    if not token_to_save and user_token in full_list_of_tokens:
        user_choice = ask_to_save_token_message(lang_state)
        if user_choice:
            database_user_data.insert_into_save_tb(encrypt(str(user_id)), encrypt(user_token))


def check_if_has_duplicates_desc(lst):
    seen = set()
    for item in lst:
        if item[0] in seen:
            return True
        else:
            seen.add(item[0])

    return False


def sync_tables_loop(remote_connection, table, lst):
    for tuple_row in lst:
        database_user_data.insert_replace_into_tb(*tuple_row)
        remote_connection.insert_update_password_data(table, *tuple_row)


def correct_lst_unite(lst1, lst2):
    lst1.extend([tuple_row for tuple_row in lst2 if tuple_row[0] not in [descr[0] for descr in lst1]])
    return lst1


def change_local_token(lang_state, application_window):
    remote_connection = result_of_connection(lang_state)

    if remote_connection is None:
        return

    full_list_of_tokens = remote_connection.select_all_tokens()

    while True:
        exit_status = try_token_change(lang_state, application_window, remote_connection, full_list_of_tokens)

        if exit_status == 'Exit from token dialog box':
            return


def try_token_change(language, app, remote_ids, remote_tokens):
    user_token = token_input_message(language, app)

    if user_token is None:
        return 'Exit from token dialog box'

    user_id = remote_ids.select_id_by_token(encrypt(user_token))

    if user_token in remote_tokens:
        if ask_to_save_new_token(language):
            database_user_data.truncate_saved_token()
            database_user_data.insert_into_save_tb(encrypt(str(user_id)), encrypt(user_token))
            successfully_changed_token_message(language)
        else:
            was_not_changed_token_message(language)
        return 'Exit from token dialog box'
    else:
        input_token_error_message(language)


def database_search(event, lang_state):
    user_search = search_query_input_message(lang_state)

    if user_search is None:
        return
    elif user_search == '' or len(user_search) > MAX_AUTO_PASSWORD_AND_DESC_LENGTH:
        invalid_search_query_message(lang_state)
        return

    data_list = retrieve_data_for_build_table_interface(lang_state, column_number=3, user_query=user_search)

    if data_list['data'].empty:
        no_matches_for_search_message(lang_state, user_search)
        return

    search_screen(lang_state, user_search, data_list)


def password_strength_checker(event, lang_state):
    password_strength_screen(lang_state)
