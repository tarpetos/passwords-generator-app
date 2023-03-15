import json
import os

ROOT_PATH = os.path.expanduser('~/.passwords/')

LOCALIZATION_FILE = os.path.expanduser(f'{ROOT_PATH}localization.json')
LOCALIZATION_DATA = {
    "EN": {
        "labels": {
            "password_description_label": "For what this password should be?: ",
            "password_length_label": "Enter password length:",
            "repeatable_label": "Can be repeatable characters in password (y/n)?:",
            "result_password_label": "GENERATED PASSWORD",
            "option_menu_label": "Choose password difficulty:"
        },
        "radio_buttons_labels": {
            "all_symbols_label": "All symbols",
            "only_letters_label": "Only letters",
            "only_digits_label": "Only digits",
            "letters_digits_label": "Letters & digits",
            "letters_signs_label": "Letters & signs",
            "digits_signs_label": "Digits & signs"
        },
        "buttons": {
            "generate_btn": "Generate",
            "copy_btn": "Copy password",
            "clear_btn": "Clear all",
            "write_to_db_btn": "Write to database",
            "simple_mode_btn": "Simple mode",
            "hard_mode_btn": "Hard mode",
            "move_to_table_btn": "Show table >>>>",
            "synchronize_data_btn": "Synchronization",
            "change_token_btn": "Change token",
            "return_to_main_btn": "<<<< Back",
            "reload_table_btn": "Reload",
            "update_table_btn": "Update record",
            "delete_record_btn": "Delete",
            "ukrainian_lang_btn": "UA",
            "english_lang_btn": "EN",
            "quit_btn": "Quit"
        },
        "table_column_names": {
            "id": "UNIQUE IDENTIFIER",
            "description": "PASSWORD DESCRIPTION",
            "password": "PASSWORD",
            "length": "PASSWORD LENGTH",
            "has_repeatable": "CONTAIN REPEATED CHARACTERS?",
            "add_date": "RECORD ADDITION DATE",
            "update_date": "RECORD CHANGE DATE",
            "delete_date": "RECORD DELETION DATE"
        },
        "switches": {
            "write_to_db_switch": "Write to database?"
        },
        "symbols_option_menu": [
            "Extremely unreliable",
            "Very easy",
            "Easy",
            "Below average",
            "Average",
            "Strong",
            "Very strong",
            "Extremely reliable"
        ],
        "repeatable_segment_btn": [
            "Yes",
            "No"
        ],
        "tooltips": {
            "write_to_db_switch_tip": "Enable/disable writing to the database. "
                                      "The password will be stored in the database "
                                      "only if the description field is not empty.",
        }
    },
    "UA": {
        "labels": {
            "password_description_label": "Яке призначення цього пароля?: ",
            "password_length_label": "Введіть, якої довжини має бути пароль:",
            "repeatable_label": "Чи можуть бути повторювані символи в паролі (т/н)?:",
            "result_password_label": "ЗГЕНЕРОВАНИЙ ПАРОЛЬ",
            "option_menu_label": "Виберіть складність пароля:"
        },
        "radio_buttons_labels": {
            "all_symbols_label": "Усі символи",
            "only_letters_label": "Тільки букви",
            "only_digits_label": "Тільки цифри",
            "letters_digits_label": "Букви і цифри",
            "letters_signs_label": "Букви і знаки",
            "digits_signs_label": "Цифри і знаки"
        },
        "buttons": {
            "generate_btn": "Згенерувати пароль",
            "copy_btn": "Скопіювати пароль",
            "clear_btn": "Очистити всі поля",
            "write_to_db_btn": "Записати до бази даних",
            "simple_mode_btn": "Простий режим",
            "hard_mode_btn": "Складний режим",
            "move_to_table_btn": "Показати таблицю >>>>",
            "synchronize_data_btn": "Синхронізація",
            "change_token_btn": "Змінити токен",
            "return_to_main_btn": "<<<< Назад",
            "reload_table_btn": "Оновити",
            "update_table_btn": "Змінити запис",
            "delete_record_btn": "Видалити",
            "ukrainian_lang_btn": "УКР",
            "english_lang_btn": "АНГЛ",
            "quit_btn": "Вихід"
        },
        "table_column_names": {
            "id": "УНІКАЛЬНИЙ ІДЕНТИФІКАТОР",
            "description": "ОПИС ПАРОЛЯ",
            "password": "ПАРОЛЬ",
            "length": "ДОВЖИНА ПАРОЛЯ",
            "has_repeatable": "МІСТИТЬ ПОВТОРЮВАНІ СИМВОЛИ?",
            "add_date": "ДАТА ДОДАВАННЯ ЗАПИСУ",
            "update_date": "ДАТА ЗМІНИ ЗАПИСУ",
            "delete_date": "ДАТА ВИДАЛЕННЯ ЗАПИСУ"
        },
        "switches": {
            "write_to_db_switch": "Записати до бази даних?"
        },
        "symbols_option_menu": [
            "Мінімально надійний",
            "Дуже простий",
            "Простий",
            "Нижче середнього",
            "Середній",
            "Надійний",
            "Дуже надійний",
            "Максимально надійний"
        ],
        "repeatable_segment_btn": [
            "Так",
            "Ні"
        ],
        "tooltips": {
            "write_to_db_switch_tip": "Ввімкнути/вимкнути запис до бази даних. "
                                      "Пароль буде збережено до бази даних тільки, якщо поле опису не буде пустим."
        }
    }
}


def create_directory():
    if not os.path.exists(ROOT_PATH):
        os.mkdir(os.path.join(ROOT_PATH))


def load_json_localization_data():
    create_directory()
    if os.path.exists(LOCALIZATION_FILE):
        with open(LOCALIZATION_FILE) as translation_file:
            translation_data = json.load(translation_file)
            return translation_data

    with open(LOCALIZATION_FILE, 'w') as translation_file:
        json.dump(LOCALIZATION_DATA, translation_file, indent=4)
    return LOCALIZATION_DATA


all_json_localization_data = load_json_localization_data()
