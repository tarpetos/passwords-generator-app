# import json

# LOCALIZATION_FILE = os.path.expanduser(f'{ROOT_PATH}localization.json')
LOCALIZATION_DATA = {
    "EN": {
        "labels": {
            "password_description_label": "Enter password description: ",
            "password_length_label": "Choose password length:",
            "repeatable_label": "Can be repeatable characters in password?:",
            "result_password_label": "GENERATED PASSWORD",
            "option_menu_label": "Choose password difficulty:",
        },
        "radio_buttons_labels": {
            "all_symbols_label": "All symbols",
            "only_letters_label": "Only letters",
            "only_digits_label": "Only digits",
            "letters_digits_label": "Letters & digits",
            "letters_signs_label": "Letters & signs",
            "digits_signs_label": "Digits & signs",
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
            "change_encryption_token_btn": "Change encryption key",
            "return_to_main_btn": "<<<< Back",
            "reload_table_btn": "Reload",
            "update_table_btn": "Update record",
            "delete_record_btn": "Delete",
            "new_alphabet_btn": "Custom alphabet",
            "quit_btn": "Quit",
        },
        "table_column_names": [
            "UNIQUE IDENTIFIER",
            "PASSWORD DESCRIPTION",
            "PASSWORD",
            "PASSWORD LENGTH",
            "CONTAIN REPEATED CHARACTERS?",
            "RECORD ADDITION DATE",
            "RECORD CHANGE DATE",
            "RECORD DELETION DATE",
        ],
        "switches": {"write_to_db_switch": "Write to database?"},
        "symbols_option_menu": [
            "Extremely unreliable",
            "Very easy",
            "Easy",
            "Below average",
            "Average",
            "Strong",
            "Very strong",
            "Extremely reliable",
        ],
        "repeatable_segment_btn": ["Yes", "No"],
        "tooltips": {
            "all_symbols_radio_btn_tip": "Possible letters: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Possible digits: 0123456789\n"
            "Possible signs: !#$%()*+,-./:;=?@[\]^_{|}~",
            "only_letters_radio_btn_tip": "Possible letters: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "only_digits_radio_btn_tip": "Possible digits: 0123456789",
            "letters_digits_radio_btn_tip": "Possible letters: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Possible digits: 0123456789",
            "letters_signs_radio_btn_tip": "Possible letters: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Possible signs: !#$%()*+,-./:;=?@[\]^_{|}~",
            "digits_signs_radio_btn_tip": "Possible digits: 0123456789\n"
            "Possible signs: !#$%()*+,-./:;=?@[\]^_{|}~",
            "write_to_db_switch_tip": "Enable/disable writing to the database. "
            "The password will be stored in the database "
            "only if the description field is not empty.",
        },
        "messageboxes": {
            "ok_button_value": "Ok",
            "error_message": {
                "invalid_password_description": {
                    "title": "Invalid input",
                    "text": "Length of password description field have to be in range from 1 to 500!",
                },
                "empty_result_input": {
                    "title": "Field is unfilled",
                    "text": "No password in result field!!!\nGenerate or type it and then write to database.",
                },
                "unexpected_database_error": {
                    "title": "Database error",
                    "text": "Unexpected error while writing to database!",
                },
                "duplicate_description": {
                    "title": "Invalid input",
                    "text": "Password with such description already exists!\n"
                    "Try to type another description or change existent and repeat your choice.",
                },
            },
            "warning_message": {
                "nothing_to_copy": {
                    "title": "Copy",
                    "text": "Password field is empty. Nothing to copy!",
                },
                "empty_table": {
                    "title": "Empty table",
                    "text": "There are no records in the local table!",
                },
                "invalid_id_input": {
                    "title": "Invalid input",
                    "text": "No ID with such value in the table! Try again.",
                },
                "invalid_search_query": {
                    "title": "Invalid search query",
                    "text": "Search query cannot be empty space or has more than 500 symbols in it! Try again.",
                },
            },
            "yes_no_message": {
                "ask_write_to_database": {
                    "title": "Writing to database...",
                    "text": "Would you like to write this data to database?",
                },
                "ask_if_record_exist": {
                    "title": "Accept or decline writing...",
                    "text": "A record with such description already exists. "
                    "Are you sure you want to change the password associated with this record?",
                },
            },
            "yes_no_message_options": ("Yes", "No"),
            "info_message": {
                "successful_write_to_database": {
                    "title": "Database info",
                    "text": "All password data was written to database!",
                },
                "successful_update": {
                    "title": "Table update",
                    "text": "You have changed the data in the table!\nChanges saved successfully.",
                },
                "successful_delete": {
                    "title": "Record deleting",
                    "text": "The record with the specified ID has been deleted successfully!",
                },
                "successful_remake_table": {
                    "title": "Table regeneration",
                    "text": "Table was successfully completely was regenerated! "
                    "Reload the table to reflect the changes.",
                },
                "successful_key_change": {
                    "title": "Key changed",
                    "text": "Encryption key was successfully changed! All passwords were re-encrypted.",
                },
                "no_matches_for_search": {
                    "title": "No matches",
                    "text": "No mathes for query: ",
                },
            },
            "ok_cancel_message": {
                "remake_table": {
                    "title": "Reset table",
                    "text": "Are you sure you want to regenerate the table (all local data will be lost)?",
                },
                "change_encryption_key": {
                    "title": "Key change",
                    "text": "Are you sure you want to change the encryption key for passwords? "
                    "The data in the current table will first be decrypted using the old key, and then encrypted "
                    "again. After that, the old key will be deleted. History of generation will be cleared.",
                },
            },
            "ok_cancel_message_options": ("Ok", "Cancel"),
            "input_message": {
                "id_input": {
                    "title": "ID input",
                    "text": "Enter the ID of the record you want to delete...",
                },
                "search_query_input": {
                    "title": "Search",
                    "text": "Enter a search query (description of the password you want to find).\n"
                    "Search is case-insensitive.\n",
                },
            },
        },
        "toplevel_windows": {
            "loading_window_data": "Please wait...",
            "history_window_data": "This table is updated automatically. "
            "When the number of records reaches 5000, then the oldest 2500 among "
            "all records will be deleted.\n"
            "Changes to this table have no effect on the main table.",
            "search_window_data": "Search results for query: ",
            "strength_window_data": {
                "enter_label": "Enter password that you want to check for strength: ",
                "shanon_score_label": "Score on a scale from 0 to 100 (Shannon Entropy): ",
                "ai_score_label": "Score on a scale from 0 to 100 (ChatGPT Algorithm): ",
                "average_score_label": "Average score: ",
                "reliability_label": "Reliability level: ",
            },
            "alphabet_window_data": {
                "labels": {
                    "letters_label": "Enter letters: ",
                    "digits_label": "Enter digits: ",
                    "punctuation_label": "Enter punctuation or signs:",
                },
                "buttons": {
                    "close": "Close",
                    "save_alphabet_btn": "Save new alphabet",
                    "reset_alphabet_btn": "Reset to default alphabet",
                },
            },
        },
    },
    "UA": {
        "labels": {
            "password_description_label": "Введіть опис паролю: ",
            "password_length_label": "Виберіть, якої довжини має бути пароль:",
            "repeatable_label": "Чи можуть бути повторювані символи в паролі?:",
            "result_password_label": "ЗГЕНЕРОВАНИЙ ПАРОЛЬ",
            "option_menu_label": "Виберіть складність пароля:",
        },
        "radio_buttons_labels": {
            "all_symbols_label": "Усі символи",
            "only_letters_label": "Тільки букви",
            "only_digits_label": "Тільки цифри",
            "letters_digits_label": "Букви і цифри",
            "letters_signs_label": "Букви і знаки",
            "digits_signs_label": "Цифри і знаки",
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
            "change_encryption_token_btn": "Змінити ключ шифрування",
            "return_to_main_btn": "<<<< Назад",
            "reload_table_btn": "Оновити",
            "update_table_btn": "Змінити запис",
            "delete_record_btn": "Видалити",
            "new_alphabet_btn": "Власний алфавіт",
            "quit_btn": "Вихід",
        },
        "table_column_names": [
            "УНІКАЛЬНИЙ ІДЕНТИФІКАТОР",
            "ОПИС ПАРОЛЯ",
            "ПАРОЛЬ",
            "ДОВЖИНА ПАРОЛЯ",
            "МІСТИТЬ ПОВТОРЮВАНІ СИМВОЛИ?",
            "ДАТА ДОДАВАННЯ ЗАПИСУ",
            "ДАТА ЗМІНИ ЗАПИСУ",
            "ДАТА ВИДАЛЕННЯ ЗАПИСУ",
        ],
        "switches": {"write_to_db_switch": "Записати до бази даних?"},
        "symbols_option_menu": [
            "Мінімально надійний",
            "Дуже простий",
            "Простий",
            "Нижче середнього",
            "Середній",
            "Надійний",
            "Дуже надійний",
            "Максимально надійний",
        ],
        "repeatable_segment_btn": ["Так", "Ні"],
        "tooltips": {
            "all_symbols_radio_btn_tip": "Ймовірні букви: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Ймовірні цифри: 0123456789\n"
            "Ймовірні знаки: !#$%()*+,-./:;=?@[\]^_{|}~",
            "only_letters_radio_btn_tip": "Ймовірні букви: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "only_digits_radio_btn_tip": "Ймовірні цифри: 0123456789",
            "letters_digits_radio_btn_tip": "Ймовірні букви: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Ймовірні цифри: 0123456789",
            "letters_signs_radio_btn_tip": "Ймовірні букви: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Ймовірні знаки: !#$%()*+,-./:;=?@[\]^_{|}~",
            "digits_signs_radio_btn_tip": "Ймовірні цифри: 0123456789\n"
            "Ймовірні знаки: !#$%()*+,-./:;=?@[\]^_{|}~",
            "write_to_db_switch_tip": "Ввімкнути/вимкнути запис до бази даних. "
            "Пароль буде збережено до бази даних тільки, якщо поле опису не буде пустим.",
        },
        "messageboxes": {
            "ok_button_value": "Гаразд",
            "error_message": {
                "invalid_password_description": {
                    "title": "Некоректний ввід",
                    "text": "Кількість символів в полі опису пароля має знаходитись в межах від 1 до 500!",
                },
                "empty_result_input": {
                    "title": "Незаповнене поле",
                    "text": "Пароль відсутній!!!\nЗгенеруйте або введіть його і тоді запишіть до бази даних.",
                },
                "unexpected_database_error": {
                    "title": "Помилка бази даних",
                    "text": "Неочікувана помилка під час запису даних до бази!",
                },
                "duplicate_description": {
                    "title": "Некоректний ввід",
                    "text": "Пароль із заданим описом уже існує!\n"
                    "Спробуйте вибрати інший опис або змінити існуючий і повторити ваш вибір.",
                },
            },
            "warning_message": {
                "nothing_to_copy": {
                    "title": "Копіювання",
                    "text": "Поле паролю пусте. Дані для копіювання відсутні!",
                },
                "empty_table": {
                    "title": "Таблиця пуста",
                    "text": "У локальній таблиці немає записів!",
                },
                "invalid_id_input": {
                    "title": "Некоректний ввід",
                    "text": "ID таким значенням відсутній у таблиці. Спробуйте ще раз.",
                },
                "invalid_search_query": {
                    "title": "Некоректний пошуковий запит",
                    "text": "Пошуковий запит не може бути пустим місцем або мати більше ніж 500 символів! "
                    "Спробуйте ще раз.",
                },
            },
            "yes_no_message": {
                "ask_write_to_database": {
                    "title": "Запис до бази даних...",
                    "text": "Ви хочете записати дані до бази даних?",
                },
                "ask_if_record_exist": {
                    "title": "Прийняти або відхилити записування...",
                    "text": "Запис з таким описом вже існує.\n "
                    "Ви впевнені, що хочете змінити пароль, який відноситься до цього запису?",
                },
            },
            "yes_no_message_options": ("Так", "Ні"),
            "info_message": {
                "successful_write_to_database": {
                    "title": "Інформація про базу даних",
                    "text": "Дані успішно записано до бази даних!",
                },
                "successful_update": {
                    "title": "Зміна таблиці",
                    "text": "Ви змінили дані в таблиці! Зміни записано успішно.",
                },
                "successful_delete": {
                    "title": "Видалення запису",
                    "text": "Запис зі вказаним ID видалено успішно!",
                },
                "successful_remake_table": {
                    "title": "Регенерація таблиці",
                    "text": "Таблиця була успішно повністю перегенерована! Оновіть таблицю для відображення змін. ",
                },
                "successful_key_change": {
                    "title": "Ключ змінено",
                    "text": "Ключ шифрування успішно змінено! Всі паролі було перешифровано.",
                },
                "no_matches_for_search": {
                    "title": "Відсутні збіги",
                    "text": "Збіги відсутні на запит: ",
                },
            },
            "ok_cancel_message": {
                "remake_table": {
                    "title": "Скидання таблиці",
                    "text": "Ви впевнені, що хочете перегенерувати таблицю (усі локальні дані буде втрачено)?",
                },
                "change_encryption_key": {
                    "title": "Зміна ключа",
                    "text": "Ви впевнені, що хочете змінити ключ шифрування паролів? "
                    "Дані у поточній таблиці спочатку будуть дешифровані за старим ключем, а потім зашифровані "
                    "знову. Після цього старий ключ буде видалено. Історія генерації буде очищена",
                },
            },
            "ok_cancel_message_options": ("Гаразд", "Відміна"),
            "input_message": {
                "id_input": {
                    "title": "Ввід ID",
                    "text": "Введіть ID запису, який ви хочете видалити...",
                },
                "search_query_input": {
                    "title": "Пошук",
                    "text": "Введіть пошуковий запит (опис пароля, який хочете знайти).\nПошук є регістро незалежним.\n",
                },
            },
        },
        "toplevel_windows": {
            "loading_window_data": "Очікуйте, будь ласка...",
            "history_window_data": "Ця таблиця оновлюється автоматично. Коли кількість записів досягає 5000, "
            "то 2500 старіших серед усіх записів "
            "будуть видалені.\nЗміни в цій таблиці ніяк не впливають на головну таблицю.",
            "search_window_data": "Результати пошуку на запит: ",
            "strength_window_data": {
                "enter_label": "Введіть пароль, який ви хочете перевірити на надійність: ",
                "shanon_score_label": "Оцінка по шкалі від 0 до 100 (Ентропія Шенона): ",
                "ai_score_label": "Оцінка по шкалі від 0 до 100 (Алгоритм ChatGPT): ",
                "average_score_label": "Середній показник: ",
                "reliability_label": "Рівень надійності: ",
            },
            "alphabet_window_data": {
                "labels": {
                    "letters_label": "Введіть букви: ",
                    "digits_label": "Введіть цифри: ",
                    "punctuation_label": "Введіть пунктуацію або знаки:",
                },
                "buttons": {
                    "close": "Закрити",
                    "save_alphabet_btn": "Зберегти новий алфавіт",
                    "reset_alphabet_btn": "Відновити то стандартного алфавіту",
                },
            },
        },
    },
    "PL": {
        "labels": {
            "password_description_label": "Wpisz opis hasła:",
            "password_length_label": "Wybierz długość hasła:",
            "repeatable_label": "Czy w haśle mogą występować powtarzające się znaki?:",
            "result_password_label": "WYGENEROWANE HASŁO",
            "option_menu_label": "Wybierz trudność hasła:",
        },
        "radio_buttons_labels": {
            "all_symbols_label": "Wszystkie symbole",
            "only_letters_label": "Tylko litery",
            "only_digits_label": "Tylko cyfry",
            "letters_digits_label": "Litery i cyfry",
            "letters_signs_label": "Litery i znaki",
            "digits_signs_label": "Cyfry i znaki",
        },
        "buttons": {
            "generate_btn": "Generuj",
            "copy_btn": "Kopiuj hasło",
            "clear_btn": "Wyczyść wszystko",
            "write_to_db_btn": "Zapisz do bazy danych",
            "simple_mode_btn": "Tryb prosty",
            "hard_mode_btn": "Tryb zaawansowany",
            "move_to_table_btn": "Pokaż tabelę >>>>",
            "synchronize_data_btn": "Synchronizuj",
            "change_encryption_token_btn": "Zmień klucz szyfrowania",
            "return_to_main_btn": "<<<< Powrót",
            "reload_table_btn": "Odśwież",
            "update_table_btn": "Zaktualizuj rekord",
            "delete_record_btn": "Usuń",
            "new_alphabet_btn": "Własny alfabet",
            "quit_btn": "Wyjście",
        },
        "table_column_names": [
            "UNIKALNY IDENTYFIKATOR",
            "OPIS HASŁA",
            "HASŁO",
            "DŁUGOŚĆ HASŁA",
            "ZAWIERA POWTARZAJĄCE SIĘ ZNAKI?",
            "DATA DODANIA REKORDU",
            "DATA ZMIANY REKORDU",
            "DATA USUNIĘCIA REKORDU",
        ],
        "switches": {"write_to_db_switch": "Zapisać do bazy danych?"},
        "symbols_option_menu": [
            "Ekstremalnie niesolidne",
            "Bardzo łatwe",
            "Łatwe",
            "Poniżej przeciętnej",
            "Przeciętne",
            "Silne",
            "Bardzo silne",
            "Ekstremalnie solidne",
        ],
        "repeatable_segment_btn": ["Tak", "Nie"],
        "tooltips": {
            "all_symbols_radio_btn_tip": "Możliwe litery: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Możliwe cyfry: 0123456789\n"
            "Możliwe znaki: !#$%()*+,-./:;=?@[\]^_{|}~",
            "only_letters_radio_btn_tip": "Możliwe litery: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "only_digits_radio_btn_tip": "Możliwe cyfry: 012345678",
            "letters_digits_radio_btn_tip": "Możliwe litery: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Możliwe cyfry: 0123456789",
            "letters_signs_radio_btn_tip": "Możliwe litery: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"
            "Możliwe znaki: !#$%()+,-./:;=?@[]^_{|}~",
            "digits_signs_radio_btn_tip": "Możliwe cyfry: 0123456789\n"
            "Możliwe znaki: !#$%()+,-./:;=?@[]^_{|}~",
            "write_to_db_switch_tip": "Włącz/wyłącz zapisywanie do bazy danych. "
            "Hasło będzie przechowywane w bazie danych "
            "tylko jeśli pole opis nie będzie puste.",
        },
        "messageboxes": {
            "ok_button_value": "Ok",
            "error_message": {
                "invalid_password_description": {
                    "title": "Nieprawidłowe dane wejściowe",
                    "text": "Długość pola opis hasła musi zawierać się w przedziale od 1 do 500!",
                },
                "empty_result_input": {
                    "title": "Nie wypełnione pole",
                    "text": "Brak hasła w polu wyniku!!!\nWygeneruj lub wpisz hasło, a następnie zapisz je w bazie danych.",
                },
                "unexpected_database_error": {
                    "title": "Błąd bazy danych",
                    "text": "Nieoczekiwany błąd podczas zapisywania w bazie danych!",
                },
                "duplicate_description": {
                    "title": "Nieprawidłowe dane wejściowe",
                    "text": "Hasło o takim opisie już istnieje!\n"
                    "Spróbuj wprowadzić inny opis lub zmień istniejący i spróbuj ponownie.",
                },
            },
            "warning_message": {
                "nothing_to_copy": {
                    "title": "Kopiowanie",
                    "text": "Pole hasła jest puste. Nic do skopiowania!",
                },
                "empty_table": {
                    "title": "Pusta tabela",
                    "text": "W tabeli lokalnej nie ma żadnych rekordów!",
                },
                "invalid_id_input": {
                    "title": "Nieprawidłowe dane wejściowe",
                    "text": "Nie ma ID o takiej wartości w tabeli! Spróbuj ponownie.",
                },
                "invalid_search_query": {
                    "title": "Nieprawidłowe zapytanie",
                    "text": "Zapytanie nie może składać się wyłącznie z pustych spacji lub mieć więcej niż 500 znaków! Spróbuj ponownie.",
                },
            },
            "yes_no_message": {
                "ask_write_to_database": {
                    "title": "Zapisywanie w bazie danych...",
                    "text": "Czy chcesz zapisać te dane w bazie danych?",
                },
                "ask_if_record_exist": {
                    "title": "Akceptuj lub odrzuć zapisywanie...",
                    "text": "Rekord o takim opisie już istnieje.",
                },
            },
            "yes_no_message_options": ("Tak", "Nie"),
            "info_message": {
                "successful_write_to_database": {
                    "title": "Informacja o bazie danych",
                    "text": "Wszystkie dane hasła zostały zapisane do bazy danych!",
                },
                "successful_update": {
                    "title": "Aktualizacja tabeli",
                    "text": "Zmieniłeś dane w tabeli!\nZmiany zostały pomyślnie zapisane.",
                },
                "successful_delete": {
                    "title": "Usuwanie rekordu",
                    "text": "Rekord o określonym ID został pomyślnie usunięty!",
                },
                "successful_remake_table": {
                    "title": "Regeneracja tabeli",
                    "text": "Tabela została pomyślnie zregenerowana! "
                    "Przeładuj tabelę, aby odzwierciedlić zmiany.",
                },
                "successful_key_change": {
                    "title": "Klucz zmieniony",
                    "text": "Klucz szyfrowania został pomyślnie zmieniony! Wszystkie hasła zostały ponownie zaszyfrowane.",
                },
                "no_matches_for_search": {
                    "title": "Brak wyników",
                    "text": "Brak wyników dla zapytania: ",
                },
            },
            "ok_cancel_message": {
                "remake_table": {
                    "title": "Resetuj tabelę",
                    "text": "Czy na pewno chcesz zregenerować tabelę (wszystkie lokalne dane zostaną utracone)?",
                },
                "change_encryption_key": {
                    "title": "Zmień klucz",
                    "text": "Czy na pewno chcesz zmienić klucz szyfrowania haseł? "
                    "Dane w bieżącej tabeli zostaną najpierw odszyfrowane za pomocą starego klucza, a następnie zaszyfrowane "
                    "ponownie. Po tym stary klucz zostanie usunięty. Historia generacji zostanie wyczyszczona.",
                },
            },
            "ok_cancel_message_options": ("Ok", "Anuluj"),
            "input_message": {
                "id_input": {
                    "title": "Wprowadź ID",
                    "text": "Wprowadź ID rekordu, który chcesz usunąć...",
                },
                "search_query_input": {
                    "title": "Szukaj",
                    "text": "Wprowadź zapytanie wyszukiwania (opis hasła, którego szukasz).\n"
                    "Wyszukiwanie jest niezależne od wielkości liter.\n",
                },
            },
        },
        "toplevel_windows": {
            "loading_window_data": "Proszę czekać...",
            "history_window_data": "Ta tabela jest aktualizowana automatycznie. "
            "Kiedy liczba rekordów osiągnie 5000, najstarsze 2500 spośród "
            "wszystkich rekordów zostaną usunięte.\n"
            "Zmiany w tej tabeli nie mają wpływu na główną tabelę.",
            "search_window_data": "Wyniki wyszukiwania dla zapytania: ",
            "strength_window_data": {
                "enter_label": "Wprowadź hasło, które chcesz sprawdzić pod kątem siły: ",
                "shanon_score_label": "Wynik w skali od 0 do 100 (Entropia Shannona): ",
                "ai_score_label": "Wynik w skali od 0 do 100 (Algorytm ChatGPT): ",
                "average_score_label": "Średni wynik: ",
                "reliability_label": "Poziom niezawodności: ",
            },
            "alphabet_window_data": {
                "labels": {
                    "letters_label": "Wprowadź litery: ",
                    "digits_label": "Wprowadź cyfry: ",
                    "punctuation_label": "Wprowadź interpunkcję lub znaki: ",
                },
                "buttons": {
                    "close": "Zamknij",
                    "save_alphabet_btn": "Zapisz nowy alfabet",
                    "reset_alphabet_btn": "Przywróć domyślny alfabet",
                },
            },
        },
    },
}

# def create_directory():
#     if not os.path.exists(ROOT_PATH):
#         os.mkdir(os.path.join(ROOT_PATH))
#
#
# def load_LOCALIZATION_DATA():
#     create_directory()
#     if os.path.exists(LOCALIZATION_FILE):
#         with open(LOCALIZATION_FILE) as translation_file:
#             saved_data = json.load(translation_file)
#             return saved_data
#
#     with open(LOCALIZATION_FILE, 'w') as translation_file:
#         json.dump(LOCALIZATION_DATA, translation_file, indent=4)
#     return LOCALIZATION_DATA


# LOCALIZATION_DATA = LOCALIZATION_DATA
