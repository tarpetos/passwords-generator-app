from ..app_translation.load_data_for_localization import LOCALIZATION_DATA
from ..application_graphical_interface.expanded_ctk_input_dialog import (
    ExpandedCTkInputDialog,
)
from ..application_graphical_interface.custom_messagebox import (
    show_error,
    ask_yes_no,
    ask_ok_cancel,
    show_info,
    show_warning,
)


# ###################################################### ERRORS ###################################################### #
def invalid_password_description_message(lang_state: str):
    show_error(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "invalid_password_description"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "invalid_password_description"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def empty_result_input_message(lang_state: str):
    show_error(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "empty_result_input"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "empty_result_input"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def duplicate_description_message(lang_state: str):
    show_error(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "duplicate_description"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "duplicate_description"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def unexpected_database_error_message(lang_state: str):
    show_error(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "unexpected_database_error"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["error_message"][
            "unexpected_database_error"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


# ##################################################### WARNINGS ##################################################### #
def nothing_to_copy_message(lang_state: str):
    show_warning(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "nothing_to_copy"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "nothing_to_copy"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def empty_table_message(lang_state: str):
    show_warning(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"]["empty_table"][
            "title"
        ],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"]["empty_table"][
            "text"
        ],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def invalid_id_input_message(lang_state: str):
    show_warning(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "invalid_id_input"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "invalid_id_input"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def invalid_search_query_message(lang_state: str):
    show_warning(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "invalid_search_query"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["warning_message"][
            "invalid_search_query"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


# ####################################################### INFO ####################################################### #
def successful_write_to_database_message(lang_state: str):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_write_to_database"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_write_to_database"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def successful_update_message(lang_state: str):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_update"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_update"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def successful_delete_message(lang_state: str):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_delete"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_delete"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def successful_remake_table_message(lang_state: str):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_remake_table"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_remake_table"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def successful_key_change_message(lang_state: str):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_key_change"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "successful_key_change"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
    )


def no_matches_for_search_message(lang_state, search_query):
    show_info(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "no_matches_for_search"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["info_message"][
            "no_matches_for_search"
        ]["text"]
        + search_query,
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_button_value"],
        wrap_length=500,
    )


# #################################################### ASK YES NO #################################################### #
def ask_write_to_database_message(lang_state: str):
    user_choice = ask_yes_no(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message"][
            "ask_write_to_database"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message"][
            "ask_write_to_database"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message_options"],
    )

    return user_choice


def ask_if_record_exist_message(lang_state: str):
    user_choice = ask_yes_no(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message"][
            "ask_if_record_exist"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message"][
            "ask_if_record_exist"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["yes_no_message_options"],
    )

    return user_choice


# ################################################## ASK OK CANCEL ################################################### #
def remake_table_message(lang_state: str):
    user_choice = ask_ok_cancel(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message"][
            "remake_table"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message"][
            "remake_table"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message_options"],
    )

    return user_choice


def change_encryption_key_message(lang_state: str):
    user_choice = ask_ok_cancel(
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message"][
            "change_encryption_key"
        ]["title"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message"][
            "change_encryption_key"
        ]["text"],
        LOCALIZATION_DATA[lang_state]["messageboxes"]["ok_cancel_message_options"],
        wrap_length=350,
    )

    return user_choice


# ################################################### INPUT DIALOG ################################################### #
def id_input_message(lang_state: str) -> str:
    user_input_choice = ExpandedCTkInputDialog(
        title=LOCALIZATION_DATA[lang_state]["messageboxes"]["input_message"][
            "id_input"
        ]["title"],
        text=LOCALIZATION_DATA[lang_state]["messageboxes"]["input_message"]["id_input"][
            "text"
        ],
        button_options=LOCALIZATION_DATA[lang_state]["messageboxes"][
            "ok_cancel_message_options"
        ],
    )

    return user_input_choice.get_input()


def search_query_input_message(lang_state: str) -> str:
    user_input_choice = ExpandedCTkInputDialog(
        title=LOCALIZATION_DATA[lang_state]["messageboxes"]["input_message"][
            "search_query_input"
        ]["title"],
        text=LOCALIZATION_DATA[lang_state]["messageboxes"]["input_message"][
            "search_query_input"
        ]["text"],
        button_options=LOCALIZATION_DATA[lang_state]["messageboxes"][
            "ok_cancel_message_options"
        ],
    )

    return user_input_choice.get_input()
