from ..app_translation.load_data_for_localization import json_localization_data
from ..application_graphical_interface.ctk_input_dialog import MyCTkInputDialog
from ..application_graphical_interface.custom_messagebox import (
    show_error, 
    ask_yes_no, 
    ask_ok_cancel, 
    show_info, 
    show_warning
)


# ###################################################### ERRORS ###################################################### #
def invalid_password_description_message(lang_state: str):
    show_error(
        json_localization_data[lang_state]['messageboxes']['error_message']['invalid_password_description']['title'],
        json_localization_data[lang_state]['messageboxes']['error_message']['invalid_password_description']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def empty_result_input_message(lang_state: str):
    show_error(
        json_localization_data[lang_state]['messageboxes']['error_message']['empty_result_input']['title'],
        json_localization_data[lang_state]['messageboxes']['error_message']['empty_result_input']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )
    
    
def duplicate_description_message(lang_state: str):
    show_error(
        json_localization_data[lang_state]['messageboxes']['error_message']['duplicate_description']['title'],
        json_localization_data[lang_state]['messageboxes']['error_message']['duplicate_description']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )
    

def unexpected_database_error_message(lang_state: str):
    show_error(
        json_localization_data[lang_state]['messageboxes']['error_message']['unexpected_database_error']['title'],
        json_localization_data[lang_state]['messageboxes']['error_message']['unexpected_database_error']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


# ##################################################### WARNINGS ##################################################### #
def nothing_to_copy_message(lang_state: str):
    show_warning(
        json_localization_data[lang_state]['messageboxes']['warning_message']['nothing_to_copy']['title'],
        json_localization_data[lang_state]['messageboxes']['warning_message']['nothing_to_copy']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def empty_table_message(lang_state: str):
    show_warning(
        json_localization_data[lang_state]['messageboxes']['warning_message']['empty_table']['title'],
        json_localization_data[lang_state]['messageboxes']['warning_message']['empty_table']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def invalid_id_input_message(lang_state: str):
    show_warning(
        json_localization_data[lang_state]['messageboxes']['warning_message']['invalid_id_input']['title'],
        json_localization_data[lang_state]['messageboxes']['warning_message']['invalid_id_input']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def invalid_search_query_message(lang_state: str):
    show_warning(
        json_localization_data[lang_state]['messageboxes']['warning_message']['invalid_search_query']['title'],
        json_localization_data[lang_state]['messageboxes']['warning_message']['invalid_search_query']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )
    

# ####################################################### INFO ####################################################### #
def successful_write_to_database_message(lang_state: str):
    show_info(
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_write_to_database']['title'],
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_write_to_database']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def successful_update_message(lang_state: str):
    show_info(
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_update']['title'],
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_update']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def successful_delete_message(lang_state: str):
    show_info(
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_delete']['title'],
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_delete']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def successful_remake_table_message(lang_state: str):
    show_info(
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_remake_table']['title'],
        json_localization_data[lang_state]['messageboxes']['info_message']['successful_remake_table']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_button_value']
    )


def no_matches_for_search_message(lang_state, search_query):
    show_info(
        json_localization_data[lang_state]['messageboxes']['info_message']['no_matches_for_search']['title'],
        json_localization_data[lang_state]['messageboxes']['info_message']['no_matches_for_search']['text'] +
        search_query,
        json_localization_data[lang_state]['messageboxes']['ok_button_value'],
        wrap_length=500
    )


# #################################################### ASK YES NO #################################################### #
def ask_write_to_database_message(lang_state: str):
    user_choice = ask_yes_no(
        json_localization_data[lang_state]['messageboxes']['yes_no_message']['ask_write_to_database']['title'],
        json_localization_data[lang_state]['messageboxes']['yes_no_message']['ask_write_to_database']['text'],
        json_localization_data[lang_state]['messageboxes']['yes_no_message_options']
    )

    return user_choice


def ask_if_record_exist_message(lang_state: str):
    user_choice = ask_yes_no(
        json_localization_data[lang_state]['messageboxes']['yes_no_message']['ask_if_record_exist']['title'],
        json_localization_data[lang_state]['messageboxes']['yes_no_message']['ask_if_record_exist']['text'],
        json_localization_data[lang_state]['messageboxes']['yes_no_message_options']
    )

    return user_choice


# ################################################## ASK OK CANCEL ################################################### #
def remake_table_message(lang_state: str):
    user_choice = ask_ok_cancel(
        json_localization_data[lang_state]['messageboxes']['ok_cancel_message']['remake_table']['title'],
        json_localization_data[lang_state]['messageboxes']['ok_cancel_message']['remake_table']['text'],
        json_localization_data[lang_state]['messageboxes']['ok_cancel_message_options']
    )

    return user_choice


# ################################################### INPUT DIALOG ################################################### #
def id_input_message(lang_state: str) -> str:
    user_input_choice = MyCTkInputDialog(
        title=json_localization_data[lang_state]['messageboxes']['input_message']['id_input']['title'],
        text=json_localization_data[lang_state]['messageboxes']['input_message']['id_input']['text'],
        button_options=json_localization_data[lang_state]['messageboxes']['ok_cancel_message_options']
    )

    return user_input_choice.get_input()


def search_query_input_message(lang_state: str) -> str:
    user_input_choice = MyCTkInputDialog(
        title=json_localization_data[lang_state]['messageboxes']['input_message']['search_query_input']['title'],
        text=json_localization_data[lang_state]['messageboxes']['input_message']['search_query_input']['text'],
        button_options=json_localization_data[lang_state]['messageboxes']['ok_cancel_message_options']
    )

    return user_input_choice.get_input()
