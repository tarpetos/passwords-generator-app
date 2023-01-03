import mysql.connector
import requests
import re
import sqlite3
import tkinter
import pyperclip

from string import digits, ascii_letters, punctuation
from tkinter.constants import END
from random import choices, sample
from tkinter.ttk import Label


from additional_modules.create_directory_files import create_directory
from additional_modules.encryption_decryption import encrypt, decrypt
from additional_modules.search_for_description_in_database import check_if_description_existing
from app_translation.en_lists_with_transalation import english_list_of_text_for_labels, \
    english_list_of_text_for_buttons, english_list_of_text_for_radiobtns, english_list_of_text_for_table_buttons, \
    english_tuple_of_columns_names
from app_translation.uk_lists_with_translation import ukrain_list_of_text_for_labels, \
    ukrain_list_of_text_for_radiobtns, ukrain_list_of_text_for_buttons, ukrain_list_of_text_for_table_buttons, \
    ukrain_tuple_of_columns_names
from change_interface_look.change_window_config import label_lang_change, radiobtn_lang_change, btn_lang_change
from app_translation.messagebox_with_lang_change import ivalid_password_usage_message, invalid_password_type_message, \
    invalid_password_value_message, invalid_value_if_no_repeatable_characters_message, input_dialog_error_message, \
    invalid_value_for_repeatable_or_not_message, input_dialog_message, ask_to_update_record_message, \
    duplicate_usage_error_message, no_update_warning_message, successful_update_message, ask_to_sync_message, \
    successful_sync_message, error_sync_message, connection_error_message, connection_timeout_message, \
    token_input_message, input_token_error_message, data_is_identical_message, ask_to_save_token_message, \
    choose_between_duplicates_message, show_warn_by_regex_message, token_server_changed_message, remake_table_message, \
    empty_table_warn, ask_to_save_new_token, successfuly_changed_token_message, was_not_changed_token_message
from app_translation.messagebox_with_lang_change import nothing_to_copy_message, empty_result_input_message, \
    ask_write_to_database_message, successful_write_to_database_message, ask_if_record_exist_message, \
    unexpected_database_error_message
from change_interface_look.wait_flowbox_style import round_rectangle, load_screen_position_size
from create_app.store_user_passwords import PasswordStore
from create_app.sync_table import RemoteDB

lang_state = True
lang_table_page_state = True
HALF_VARCHAR = 384

create_directory()
database_user_data = PasswordStore()

def english_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict):
    global lang_state
    lang_state = True

    label_lang_change(labels_dict, english_list_of_text_for_labels)
    btn_lang_change(buttons_dict, english_list_of_text_for_buttons)
    # change_en_buttons_width(buttons_dict)
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
    # change_uk_buttons_width(buttons_dict)
    radiobtn_lang_change(radiobtn_dict, ukrain_list_of_text_for_radiobtns)


def ukrainian_language_table_window_data(buttons_dict):
    global lang_table_page_state
    lang_table_page_state = False
    btn_lang_change(buttons_dict, ukrain_list_of_text_for_table_buttons)


def get_data_from_database_table() -> list:
    full_list_of_data = database_user_data.select_full_table()
    full_list_of_data = check_columns_names(full_list_of_data)

    return full_list_of_data


def check_columns_names(full_list_of_data) -> list:
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


def write_to_database(password_usage, result_password):
    if not check_password_usage_input(password_usage):
        return

    if not check_password_result_input(result_password):
        return

    user_choice = ask_write_to_database_message(lang_state)

    try:
        if user_choice:
            yes_no_choice = follow_user_if_record_repeats(database_user_data, (f'{password_usage}',))
            encryped_password = encrypt(result_password)
            if yes_no_choice == -1:
                database_user_data.insert_into_tb(
                    password_usage,
                    encryped_password,
                    len(result_password),
                    check_if_repeatable_characters_is_present(result_password)
                )
                successful_write_to_database_message(lang_state)
            elif yes_no_choice:
                database_user_data.update_existing_password(
                    encryped_password,
                    len(result_password),
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


def exclude_invalid_symblols_for_markup() -> str:
    excluded_symbols = '<>&"'
    allowed_symbols = ''.join([char for char in punctuation if char not in excluded_symbols])

    return allowed_symbols


def get_radiobtn_option(var) -> str:
    fixed_punctuation = exclude_invalid_symblols_for_markup()

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


def open_tuples_in_lst() -> list:
    get_all_id = database_user_data.select_id()

    without_tuples_lst = []

    first_tuple_index_value = 0
    for id_value in get_all_id:
        without_tuples_lst.append(id_value[first_tuple_index_value])

    return without_tuples_lst


def remove_record_from_table(application_window):
    if database_user_data.select_full_table() is None:
        empty_table_warn(lang_table_page_state)
        return

    id_list = open_tuples_in_lst()
    chosen_id = input_dialog_message(lang_table_page_state, application_window)

    if chosen_id == -1:
        if remake_table_message(lang_table_page_state):
            database_user_data.drop_table()
            database_user_data.create_table()
        return

    while True:
        if not chosen_id:
            return

        if chosen_id not in id_list:
            input_dialog_error_message(lang_table_page_state)
            chosen_id = input_dialog_message(lang_table_page_state, application_window)
        else:
            database_user_data.delete_by_id(chosen_id)
            break


def update_record_in_table() -> bool:
    return ask_to_update_record_message(lang_table_page_state)


def duplicate_usage_in_table():
    duplicate_usage_error_message(lang_table_page_state)


def nothing_to_update_in_table():
    no_update_warning_message(lang_table_page_state)


def successful_update_in_table():
    successful_update_message(lang_table_page_state)


def sync_db_data(application_window):
    remote_connection = result_of_connection(application_window)
    if remote_connection is None:
        return

    ask_to_sync = ask_to_sync_message(lang_table_page_state)

    if ask_to_sync:
        full_list_of_tokens = remote_connection.select_all_tokens()
        saved_data = database_user_data.select_from_save_tb()

        user_token = check_for_token(application_window, saved_data)
        user_id = check_for_id(remote_connection, saved_data, user_token)

        print(user_token)
        if user_token is None:
            return

        while True:
            if user_token in full_list_of_tokens:
                user_id = check_for_id(remote_connection, saved_data, user_token)
                save_token(saved_data, user_id, user_token, full_list_of_tokens)

                table_name = f'pass_gen_table_{user_id}'
                local_full_table = database_user_data.select_without_id()
                remote_full_table = remote_connection.select_pass_gen_table_without_id(table_name)

                lst_union = set(local_full_table) | set(remote_full_table)

                if sorted(local_full_table) == sorted(lst_union):
                    data_is_identical_message(lang_table_page_state)
                    return
                else:
                    temp_lst = local_full_table + remote_full_table
                    if check_if_has_duplicates_desc(temp_lst):
                        while True:
                            save_pass = choose_between_duplicates_message(lang_table_page_state, application_window)

                            if save_pass == '' or save_pass:
                                local_choice_pattern = re.compile('^(local|локально)$', re.IGNORECASE)
                                remote_choice_pattern = re.compile('^(remote|сервер)$', re.IGNORECASE)
                                if re.match(local_choice_pattern, save_pass):
                                    load_screen = app_loading_screen(application_window)
                                    local_full_table = correct_lst_unite(local_full_table, remote_full_table)
                                    sync_tables_loop(remote_connection, table_name, local_full_table)
                                    successful_sync_message(lang_table_page_state)
                                    print('local')
                                    load_screen.destroy()
                                    return
                                elif re.match(remote_choice_pattern, save_pass):
                                    load_screen = app_loading_screen(application_window)
                                    remote_full_table = correct_lst_unite(remote_full_table, local_full_table)
                                    sync_tables_loop(remote_connection, table_name, remote_full_table)
                                    successful_sync_message(lang_table_page_state)
                                    print('remote')
                                    load_screen.destroy()
                                    return
                                else:
                                    load_screen = app_loading_screen(application_window)
                                    show_warn_by_regex_message(lang_table_page_state)
                                    print('invalid')
                                    load_screen.destroy()
                            else:
                                print('else')
                                return
                    else:
                        sync_tables_loop(remote_connection, table_name, temp_lst)
                        successful_sync_message(lang_table_page_state)
                        return
            else:
                if saved_data:
                    token_server_changed_message(lang_table_page_state)
                    database_user_data.truncate_saved_token()
                    user_token = token_input_message(lang_table_page_state, application_window)
                    save_token(saved_data, user_id, user_token, full_list_of_tokens)
                else:
                    input_token_error_message(lang_table_page_state)
                    user_token = token_input_message(lang_table_page_state, application_window)

                if user_token is None:
                    return


def result_of_connection(application_window) -> RemoteDB | None:
    load_screen = app_loading_screen(application_window)
    remote_connection = control_mysql_connection()
    if remote_connection == -1:
        load_screen.destroy()
        return

    if not check_internet_connection():
        load_screen.destroy()
        connection_error_message(lang_table_page_state)
        return

    load_screen.destroy()

    return remote_connection


def control_mysql_connection() -> RemoteDB | int:
    try:
        remote_mysql_obj = RemoteDB()
        return remote_mysql_obj
    except mysql.connector.errors.OperationalError:
        connection_timeout_message(lang_table_page_state)
        return -1
    except mysql.connector.errors.DatabaseError:
        error_sync_message(lang_table_page_state)
        return -1
    except mysql.connector.errors.InterfaceError:
        error_sync_message(lang_table_page_state)
        return -1


def check_internet_connection():
    try:
        requests.get("http://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def check_for_token(app, saved_token):
    if saved_token:
        user_token = decrypt(saved_token[1])
    else:
        user_token = token_input_message(lang_table_page_state, app)

    return user_token


def check_for_id(remote_connection, saved_token, user_token):
    if saved_token:
        user_id = decrypt(saved_token[0])
    else:
        user_id = remote_connection.select_id_by_token(encrypt(user_token))

    return user_id


def save_token(token_to_save, user_id, user_token, full_list_of_tokens):
    if not token_to_save and user_token in full_list_of_tokens:
        user_choice = ask_to_save_token_message(lang_table_page_state)
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
    lst1.extend(
        [tuple_row for tuple_row in lst2 if tuple_row[0] not in [descr[0] for descr in lst1]]
    )

    return lst1


def change_local_token(application_window):
    remote_connection = result_of_connection(application_window)

    if remote_connection is None:
        return


    full_list_of_tokens = remote_connection.select_all_tokens()

    while True:
        user_token = token_input_message(lang_table_page_state, application_window)

        if user_token is None:
            break

        user_id = remote_connection.select_id_by_token(encrypt(user_token))

        if user_token in full_list_of_tokens:
            if ask_to_save_new_token(lang_table_page_state):
                database_user_data.truncate_saved_token()
                database_user_data.insert_into_save_tb(encrypt(str(user_id)), encrypt(user_token))
                successfuly_changed_token_message(lang_table_page_state)
            else:
                was_not_changed_token_message(lang_table_page_state)
            break
        else:
            input_token_error_message(lang_table_page_state)


def app_loading_screen(main_window):
    loading_screen = tkinter.Tk()
    loading_screen.overrideredirect(True)
    loading_screen.eval('tk::PlaceWindow . center')
    loading_screen.title('Loading')
    loading_screen.geometry('375x100')
    loading_screen.config(background='grey')
    loading_screen.attributes('-transparentcolor', 'grey')

    canvas = tkinter.Canvas(loading_screen, bg='grey', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    round_rectangle(0, 0, 375, 100, canvas, radius=70)

    load_screen_position_size(main_window, loading_screen)

    my_label = Label(
        canvas, text='Please wait...' if lang_table_page_state else 'Очікуйте, будь ласка...',
        font=('Arial bold', 24), foreground='white', background='black'
    )
    my_label.pack(pady=30)

    loading_screen.update()

    return loading_screen
