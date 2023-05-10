import tkinter as tk
from typing import Optional
import re
import customtkinter as ctk

import sqlite3
import pyperclip

from random import choices, sample
from string import digits, ascii_letters, punctuation
from typing import Any
from create_app.store_user_passwords import password_store
from additional_modules.encryption_decryption import encrypt
from additional_modules.toplevel_windows import search_screen, password_strength_screen
from app_translation.load_data_for_localization import localization_data

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
    for i in range(column_number):
        widget.grid_columnconfigure(i, weight=1, uniform='equal')


def set_equal_row_height(widget: tk.BaseWidget, row_number: int) -> None:
    for i in range(row_number):
        widget.grid_rowconfigure(i, weight=1, uniform='equal')


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
    return 0 < password_length <= MAX_PASSWORD_LENGTH


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
    password_length = len(password)
    repeatable = has_repeated_chars(password)
    if replaceable:
        replace_password(current_language, password_description, encrypted_password, password_length, repeatable)
    else:
        insert_password(current_language, password_description, encrypted_password, password_length, repeatable)


def generate_ask_message(current_language: str, message_type: str) -> AskMessageBox:
    return AskMessageBox(*extract_message_body(current_language, message_type))


def is_repeatable_password_description(password_description: str, password_descriptions: list[str]) -> bool:
    return password_description in password_descriptions


def replace_password(
        current_language: str,
        password_description: str,
        encrypted_password: str,
        password_length: int,
        repeatable: bool
) -> None:
    try:
        password_store.change_password_by_description(
            password_description, encrypted_password, password_length, repeatable
        )
        generate_info_message(current_language, 'successful_write_to_db')
    except sqlite3.OperationalError:
        generate_error_message(current_language, 'database_error')


def has_repeated_chars(string: str) -> bool:
    return len(set(string)) != len(string)


def generate_info_message(current_language: str, message_type: str) -> InfoMessageBox:
    return InfoMessageBox(*extract_message_body(current_language, message_type))


def insert_password(
        current_language: str,
        password_description: str,
        encrypted_password: str,
        password_length: int,
        repeatable: bool
) -> None:
    try:
        password_store.insert_password(password_description, encrypted_password, password_length, repeatable)
        generate_info_message(current_language, 'successful_write_to_db')
    except sqlite3.OperationalError:
        generate_error_message(current_language, 'database_error')


def change_background_color(btn):
    current_mode = ctk.get_appearance_mode()
    opposite_theme = OPPOSITE_THEMES.get(current_mode, {})
    btn.configure(text=opposite_theme.get('button_text', u'\u263E'))
    ctk.set_appearance_mode(opposite_theme.get('opposite_theme_name', 'Dark'))


def delete_password(current_language: str) -> None:
    passwords_ids = password_store.fetch_passwords_ids()
    while True:
        chosen_id = generate_input_dialog(current_language, 'delete_password_by_id').get_input()
        if chosen_id is None:
            return None
        if chosen_id.isdigit():
            chosen_id = int(chosen_id)
        if chosen_id not in passwords_ids:
            generate_error_message(current_language, 'invalid_password_id')
        else:
            password_store.delete_password(chosen_id)
            generate_info_message(current_language, 'successful_password_delete').wait_window()


def generate_input_dialog(current_language: str, message_type: str) -> ctk.CTkInputDialog:
    title, text = extract_message_body(current_language, message_type)
    return ctk.CTkInputDialog(title=title, text=text)


def search_passwords_by_description(event, current_language: str, table) -> None:
    searched_description = generate_input_dialog(current_language, '').get_input()
    passwords = password_store.fetch_passwords_by_description(searched_description)
    if searched_description is None:
        return None
    elif searched_description == '' or not is_valid_password_description(searched_description):
        generate_error_message(current_language, 'invalid_password_description')
        return None
    elif not passwords:
        return None
    table.build_treeview(current_language, passwords)
    table.reload_table(table, table.current_language)


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
