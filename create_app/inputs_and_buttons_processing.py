import tkinter as tk
from typing import Optional
import re
import customtkinter as ctk

import sqlite3
import mysql.connector
import pyperclip
import requests

from random import choices, sample
from string import digits, ascii_letters, punctuation
from typing import Any, Iterator
from pandas import DataFrame

from create_app.store_user_passwords import password_store

from additional_modules.encryption_decryption import encrypt, decrypt
from additional_modules.toplevel_windows import app_loading_screen, search_screen, password_strength_screen
from app_translation.load_data_for_localization import localization_data
from app_translation.messagebox_with_lang_change import invalid_value_if_no_repeatable_characters_message, \
    input_dialog_error_message, input_dialog_message, ask_to_update_record_message, \
    duplicate_usage_error_message, no_update_warning_message, successful_update_message, ask_to_sync_message, \
    successful_sync_message, error_sync_message, connection_error_message, connection_timeout_message, \
    token_input_message, input_token_error_message, data_is_identical_message, ask_to_save_token_message, \
    choose_between_duplicates_message, show_warn_by_regex_message, server_token_changed_message, remake_table_message, \
    empty_table_warn, ask_to_save_new_token, successfully_changed_token_message, was_not_changed_token_message, \
    search_query_input_message, invalid_search_query_message, \
    no_matches_for_search_message, successful_delete_message, successful_remake_table_message

# from create_app.sync_table import RemoteDB


MAX_PASSWORD_DESCRIPTION_LENGTH = 384
MAX_PASSWORD_LENGTH = 384

OPPOSITE_THEMES = {
    'Dark': {
        'button_text': u'\u263C',
        'opposite_theme_name': 'Light',
    },
    'Light': {
        'button_text': u'\u263E',
        'opposite_theme_name': 'Dark',
    },
}


def set_equal_column_width(widget: tk.BaseWidget, column_number: int) -> None:
    for column in range(column_number):
        widget.columnconfigure(column, weight=1, uniform='equal')


def set_equal_row_height(widget: tk.BaseWidget, row_number: int) -> None:
    for i in range(row_number):
        widget.rowconfigure(i, weight=1, uniform='equal')


class MessageBox(ctk.CTkToplevel):
    def __init__(self, title: Optional[str] = None, message: Optional[str] = None):
        super().__init__()
        self.title(title)
        self.geometry('400x200')
        set_equal_column_width(self, 2)
        set_equal_row_height(self, 6)

        self.label_icon = ctk.CTkLabel(self, text='')
        self.label_icon.grid(row=0, column=0, rowspan=2, columnspan=2)

        self.label_message = ctk.CTkLabel(self, text=message, font=('Arial', 18), wraplength=360)
        self.label_message.grid(row=2, column=0, rowspan=2, columnspan=2, sticky=ctk.N)

        self.wait_visibility()
        self.grab_set()


class ErrorMessageBox(MessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_icon.configure(image='::tk::icons::error')

        ok_button_font = ctk.CTkFont(family='Arial', size=18, weight='bold')
        self.ok_button = ctk.CTkButton(self, text='OK', font=ok_button_font, width=50)
        self.ok_button.configure(command=lambda: self._ok_event())
        self.ok_button.grid(row=4, column=0, rowspan=2, columnspan=2)

    def _ok_event(self) -> None:
        self.destroy()


class WarningMessageBox(MessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_icon.configure(image='::tk::icons::warning')

        ok_button_font = ctk.CTkFont(family='Arial', size=18, weight='bold')
        self.ok_button = ctk.CTkButton(self, text='OK', font=ok_button_font, width=50)
        self.ok_button.configure(command=lambda: self._ok_event())
        self.ok_button.grid(row=4, column=0, rowspan=2, columnspan=2)

    def _ok_event(self) -> None:
        self.destroy()


class InfoMessageBox(MessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_icon.configure(image='::tk::icons::information')

        ok_button_font = ctk.CTkFont(family='Arial', size=18, weight='bold')
        self.ok_button = ctk.CTkButton(self, text='OK', font=ok_button_font, width=50)
        self.ok_button.configure(command=lambda: self._ok_event())
        self.ok_button.grid(row=4, column=0, rowspan=2, columnspan=2)

    def _ok_event(self) -> None:
        self.destroy()


class AskMessageBox(MessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_icon.configure(image='::tk::icons::question')

        button_font = ctk.CTkFont(family='Arial', size=18, weight='bold')
        self.yes_button = ctk.CTkButton(self, text='YES', font=button_font, width=50)
        self.yes_button.configure(command=lambda: self._yes_event())
        self.yes_button.grid(row=4, column=0, rowspan=2, sticky=ctk.E, padx=(0, 5))

        self.no_button = ctk.CTkButton(self, text='NO', font=button_font, width=50)
        self.no_button.configure(command=lambda: self._no_event())
        self.no_button.grid(row=4, column=1, rowspan=2, sticky=ctk.W, padx=(5, 0))

        self.answer = None
        self.wait_window()

    def _yes_event(self) -> None:
        self.answer = True
        self.destroy()

    def _no_event(self) -> None:
        self.answer = False
        self.destroy()


def get_password(
        current_language: str,
        password_description: str,
        password_length: str,
        repeatable: bool,
        choice_option: int,
        password_result_entry: ctk.CTkEntry
) -> None:
    if not is_valid_password_description(password_description):
        generate_error_message(current_language, 'invalid_password_description')
        return None
    if not password_length.isdigit():
        generate_error_message(current_language, 'password_integer')
        return None
    password_length = int(password_length)
    if not is_valid_password_length(password_length):
        generate_error_message(current_language, 'invalid_password_length')
        return None

    clear_entry(password_result_entry)
    password = generate_password(get_password_alphabet(choice_option), password_length, repeatable)
    insert_value(password_result_entry, password)


def is_valid_password_description(description: str) -> bool:
    return 0 < len(description) <= MAX_PASSWORD_DESCRIPTION_LENGTH


def generate_error_message(current_language: str, message_type: str) -> None:
    ErrorMessageBox(*extract_message_body(current_language, message_type))


def extract_message_body(current_language: str, message_name: str) -> tuple[Optional[str], Optional[str]]:
    message_body = localization_data[current_language].get('messages', {}).get(message_name, {})
    return message_body.get('title'), message_body.get('message')


def is_valid_password_length(password_length: int) -> bool:
    return 0 < password_length <= MAX_PASSWORD_DESCRIPTION_LENGTH


def clear_entry(entry: ctk.CTkEntry) -> None:
    entry.delete(0, 'end')


def get_password_alphabet(choice_option: int) -> str:
    fixed_punctuation = extract_correct_punctuation()
    generated_symbols = {
        1: digits + ascii_letters + fixed_punctuation,
        2: ascii_letters,
        3: digits,
        4: digits + ascii_letters,
        5: ascii_letters + fixed_punctuation,
        6: digits + fixed_punctuation
    }
    return generated_symbols.get(choice_option, digits)


def extract_correct_punctuation() -> str:
    return re.sub(r'[<>&]', '', punctuation)


def generate_password(password_alphabet: str, password_length: int, repeatable: bool) -> str:
    return (
        ''.join(choices(password_alphabet, k=password_length)) if repeatable
        else ''.join(sample(password_alphabet, k=password_length))
    )


def insert_value(entry: ctk.CTkEntry, value: Any) -> None:
    entry.insert(0, value)


def copy_password(current_language: str, password: str) -> None:
    if is_empty_string(password):
        generate_error_message(current_language, 'nothing_to_copy')
        return None
    pyperclip.copy(password)


def is_empty_string(string: str) -> bool:
    return string == ''


def clear_entries(*entries) -> None:
    for entry in entries:
        clear_entry(entry)


def write_to_database(current_language: str, password_description: str, password: str) -> None:
    if not is_valid_password_description(password_description):
        generate_error_message(current_language, 'invalid_password_description')
        return None
    if is_empty_string(password):
        generate_error_message(current_language, 'empty_password_field')
        return None
    writeable = generate_ask_message(current_language, 'write_to_database').answer
    if not writeable:
        return None
    replaceable = False
    if is_repeatable_password_description(password_description, password_store.fetch_passwords_descriptions()):
        replaceable = generate_ask_message(current_language, 'repeatable_description').answer
    encrypted_password = encrypt(password)
    if replaceable:
        replace_password(current_language, password_description, encrypted_password)
    else:
        insert_password(current_language, password_description, encrypted_password)


def generate_ask_message(current_language: str, message_type: str) -> AskMessageBox:
    return AskMessageBox(*extract_message_body(current_language, message_type))


def is_repeatable_password_description(password_description: str, password_descriptions: list[str]) -> bool:
    return password_description in password_descriptions


def replace_password(current_language: str, password_description: str, encrypted_password: str) -> None:
    try:
        password_store.change_password_by_description(
            password_description,
            encrypted_password,
            len(encrypted_password),
            has_repeated_chars(encrypted_password)
        )
        generate_info_message(current_language, 'successful_write_to_db')
    except sqlite3.OperationalError:
        generate_error_message(current_language, 'database_error')


def has_repeated_chars(string: str) -> bool:
    return len(set(string)) == len(string)


def generate_info_message(current_language: str, message_type: str) -> InfoMessageBox:
    return InfoMessageBox(*extract_message_body(current_language, message_type))


def insert_password(current_language: str, password_description: str, encrypted_password: str) -> None:
    try:
        password_store.insert_password(
            password_description,
            encrypted_password,
            len(encrypted_password),
            has_repeated_chars(encrypted_password)
        )
        generate_info_message(current_language, 'successful_write_to_db')
    except sqlite3.OperationalError:
        generate_error_message(current_language, 'database_error')


def change_background_color(btn):
    current_mode = ctk.get_appearance_mode()
    opposite_theme = OPPOSITE_THEMES.get(current_mode, {})
    btn.configure(text=opposite_theme.get('button_text', u'\u263E'))
    ctk.set_appearance_mode(opposite_theme.get('opposite_theme_name', 'Dark'))


def table_column_names() -> tuple[list, list]:
    en_table_columns_names = [column for column in localization_data['EN']['table_column_names'].values()]
    uk_table_columns_names = [column for column in localization_data['UA']['table_column_names'].values()]

    return en_table_columns_names, uk_table_columns_names


def retrieve_data_for_build_table_interface(
        lang_state,
        column_number=5,
        user_query=None
) -> dict[str, list | Iterator[DataFrame] | DataFrame | Any]:
    column_name_localization = table_column_names()
    en_table_lst = column_name_localization[0][:column_number]
    uk_table_lst = column_name_localization[1][:column_number]

    if user_query:
        full_list_of_data = password_store.select_search_data_by_desc(user_query)
    else:
        full_list_of_data = password_store.fetch_passwords()

    return {'lang': lang_state, 'english_lst': en_table_lst, 'ukrainian_lst': uk_table_lst, 'data': full_list_of_data}


def check_for_repeatable_characters(password_alphabet, password_length, check_if_repeatable_allowed) -> str:
    if check_if_repeatable_allowed.capitalize() == 'Y' or check_if_repeatable_allowed.capitalize() == 'Т':
        return ''.join(choices(password_alphabet, k=password_length))
    elif check_if_repeatable_allowed.capitalize() == 'N' or check_if_repeatable_allowed.capitalize() == 'Н':
        return ''.join(sample(password_alphabet, k=password_length))


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


def check_if_description_existing(store_of_user_passwords, password_description):
    list_of_descriptions = store_of_user_passwords.select_descriptions()
    return password_description in list_of_descriptions


def follow_user_if_record_repeats(lang_state, description_store, password_usage) -> bool | int:
    if check_if_description_existing(description_store, password_usage):
        user_choice = ask_if_record_exist_message(lang_state)
        return user_choice
    return -1


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


# def sync_db_data(lang_state, application_window):
#     remote_connection = result_of_connection(lang_state)
#     if remote_connection is None:
#         return
#
#     ask_to_sync = ask_to_sync_message(lang_state)
#
#     if ask_to_sync:
#         full_list_of_tokens = remote_connection.select_all_tokens()
#         saved_data = database_user_data.select_from_save_tb()
#
#         user_token = check_for_token(lang_state, application_window, saved_data)
#         user_id = check_for_id(remote_connection, saved_data, user_token)
#
#         if user_token is None:
#             return
#
#         while True:
#             if user_token in full_list_of_tokens:
#                 user_id = check_for_id(remote_connection, saved_data, user_token)
#                 save_token(lang_state, saved_data, user_id, user_token, full_list_of_tokens)
#
#                 table_name = f'pass_gen_table_{user_id}'
#                 local_full_table = database_user_data.select_without_id()
#                 remote_full_table = remote_connection.select_pass_gen_table_without_id(table_name)
#
#                 lst_union = set(local_full_table) | set(remote_full_table)
#
#                 sorted_united_lst = sorted(lst_union)
#                 sorted_local_table = sorted(local_full_table)
#                 sorted_remote_table = sorted(remote_full_table)
#
#                 if sorted_local_table == sorted_united_lst and sorted_remote_table == sorted_united_lst:
#                     data_is_identical_message(lang_state)
#                     return
#
#                 temp_lst = local_full_table + remote_full_table
#                 if check_if_has_duplicates_desc(temp_lst):
#                     while True:
#                         save_pass = choose_between_duplicates_message(lang_state, application_window)
#
#                         if save_pass == '' or save_pass:
#                             local_choice_pattern = re.compile('^(local|локально)$', re.IGNORECASE)
#                             remote_choice_pattern = re.compile('^(remote|сервер)$', re.IGNORECASE)
#                             if re.match(local_choice_pattern, save_pass):
#                                 load_screen = app_loading_screen(lang_state)
#                                 local_full_table = correct_lst_unite(local_full_table, remote_full_table)
#                                 sync_tables_loop(remote_connection, table_name, local_full_table)
#                                 load_screen.destroy()
#                                 successful_sync_message(lang_state)
#                                 return
#                             elif re.match(remote_choice_pattern, save_pass):
#                                 load_screen = app_loading_screen(lang_state)
#                                 remote_full_table = correct_lst_unite(remote_full_table, local_full_table)
#                                 sync_tables_loop(remote_connection, table_name, remote_full_table)
#                                 load_screen.destroy()
#                                 successful_sync_message(lang_state)
#                                 return
#                             else:
#                                 load_screen = app_loading_screen(lang_state)
#                                 load_screen.destroy()
#                                 show_warn_by_regex_message(lang_state)
#                         else:
#                             return
#                 else:
#                     load_screen = app_loading_screen(lang_state)
#                     sync_tables_loop(remote_connection, table_name, temp_lst)
#                     load_screen.destroy()
#                     successful_sync_message(lang_state)
#                     return
#             else:
#                 if saved_data:
#                     server_token_changed_message(lang_state)
#                     database_user_data.truncate_saved_token()
#                     user_token = token_input_message(lang_state, application_window)
#                     save_token(lang_state, saved_data, user_id, user_token, full_list_of_tokens)
#                 else:
#                     input_token_error_message(lang_state)
#                     user_token = token_input_message(lang_state, application_window)
#
#                 if user_token is None:
#                     return


# def result_of_connection(lang_state) -> RemoteDB | None:
#     load_screen = app_loading_screen(lang_state)
#     remote_connection = control_mysql_connection(lang_state, load_screen)
#     if remote_connection == 'MySQL connection error':
#         return
#
#     if not check_internet_connection():
#         connection_error_message(lang_state, load_screen)
#         return
#
#     load_screen.destroy()
#
#     return remote_connection


def update_columns_via_app_interface(lang_state, all_data_from_table):
    all_data_from_table.update_data_using_table_interface(lang_state)


# def control_mysql_connection(lang_state, load_screen) -> RemoteDB | str:
#     try:
#         remote_mysql_obj = RemoteDB()
#         return remote_mysql_obj
#     except mysql.connector.errors.OperationalError:
#         connection_timeout_message(lang_state, load_screen)
#         return 'MySQL connection error'
#     except mysql.connector.errors.DatabaseError:
#         error_sync_message(lang_state, load_screen)
#         return 'MySQL connection error'
#     except mysql.connector.errors.InterfaceError:
#         error_sync_message(lang_state, load_screen)
#         return 'MySQL connection error'


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
        database_user_data.insert_update_into_tb(*tuple_row)
        remote_connection.insert_update_password_data(table, *tuple_row)


def correct_lst_unite(lst1, lst2):
    lst1.extend([tuple_row for tuple_row in lst2 if tuple_row[0] not in [descr[0] for descr in lst1]])
    return lst1


# def change_local_token(lang_state, application_window):
#     remote_connection = result_of_connection(lang_state)
#
#     if remote_connection is None:
#         return
#
#     full_list_of_tokens = remote_connection.select_all_tokens()
#
#     while True:
#         exit_status = try_token_change(lang_state, application_window, remote_connection, full_list_of_tokens)
#
#         if exit_status == 'Exit from token dialog box':
#             return


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
    elif user_search == '' or len(user_search) > MAX_PASSWORD_DESCRIPTION_LENGTH:
        invalid_search_query_message(lang_state)
        return

    data_list = retrieve_data_for_build_table_interface(lang_state, column_number=3, user_query=user_search)

    if data_list['data'].empty:
        no_matches_for_search_message(lang_state, user_search)
        return

    search_screen(lang_state, user_search, data_list)


def password_strength_checker(event, lang_state):
    password_strength_screen(lang_state)
