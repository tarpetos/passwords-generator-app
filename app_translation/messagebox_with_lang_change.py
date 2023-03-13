from tkinter import messagebox

from additional_modules.custom_input_dialogs import custom_askstring, custom_askinteger


def invalid_value_if_no_repeatable_characters_message(lang_state_check, password_alphabet):
    if lang_state_check:
        messagebox.showerror(
            'Invalid input',
            f'There are only {len(password_alphabet)} unique characters.\n' +
            'So, you need to change password length.'
        )
    else:
        messagebox.showerror(
            'Некоректний ввід',
            f'В генераторі тільки {len(password_alphabet)} унікальних символів.\n' +
            'Потрібно змінити значення довжини пароля.'
        )


def empty_table_warn(lang_state_check):
    if lang_state_check:
        messagebox.showwarning('Empty table', 'There are no records in the local table!')
    else:
        messagebox.showwarning('таблиця пуста', 'У локальній таблиці немає записів!')


def input_dialog_message(lang_state_check, application_window):
    if lang_state_check:
        user_input_choice = custom_askinteger(
            'ID input', 'Enter the ID of the record you want to delete...',
            parent=application_window, lang_state=lang_state_check
        )
    else:
        user_input_choice = custom_askinteger(
            'Ввід ID', 'Введіть ID запису, який ви хочете видалити...',
            parent=application_window, lang_state=lang_state_check
        )

    return user_input_choice


def input_dialog_error_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning('Invalid input', 'No ID with such value in the table! Try again.')
    else:
        messagebox.showwarning('Некоректний ввід', 'ID таким значенням відсутній у таблиці. Спробуйте ще раз.')


def remake_table_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askokcancel(
            'Reset table', 'Are you sure you want to regenerate the table (all local data will be lost)?'
        )
    else:
        user_choice = messagebox.askokcancel(
            'Скидання таблиці', 'Ви впевнені, що хочете перегенерувати таблицю (усі локальні дані буде втрачено)?'
        )

    print(user_choice)
    return user_choice


def ask_to_update_record_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'Accept or decline updating...',
            'You have changed descriptions and(or) passwords.\n'
            'Are you sure you want to update a full record?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Прийняти або відхилити зміну...',
            'Ви змінили опис і(або) пароль.\n'
            'Ви впевнені, що хочете змінити весь запис?'
        )

    return user_choice


def duplicate_usage_error_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror(
            'Invalid input',
            'Password with such description already exists!\n'
            'Try to type another description or change existent and repeat your choice.'
        )
    else:
        messagebox.showerror(
            'Некоректний ввід',
            'Пароль із заданим описом уже існує!\n'
            'Спробуйте вибрати інший опис або змінити існуючий і повторити ваш вибір.'
        )


def no_update_warning_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'No changes',
            'You have not changed any fields!\nNo changes have been made to the table.'
        )
    else:
        messagebox.showwarning(
            'Відсутні зміни',
            'Ви не змінили жодного поля!\nНіяких змін до таблиці не внесено.'
        )


def successful_update_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Table update',
            'You have changed the data in the table!\nChanges saved successfully.\n'
            'Reload the table to reflect the changes.'
        )
    else:
        messagebox.showinfo(
            'Зміна таблиці',
            'Ви змінили дані в таблиці! Зміни записано успішно.\n'
            'Оновіть таблицю для відображення змін.'
        )


def successful_delete_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Record deleting',
            'The record with the specified ID has been deleted successfully!'
        )
    else:
        messagebox.showinfo(
            'Видалення запису',
            'Запис зі вказаним ID видалено успішно!'
        )


def successful_remake_table_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Table regeneration',
            'Table was successfully completely was regenerated! Reload the table to reflect the changes.'
        )
    else:
        messagebox.showinfo(
            'Перегенерація таблиці',
            'Таблиця була успішно повністю перегенерована! Оновіть таблицю для відображення змін.'
        )


def ask_to_sync_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'Database synchronization',
            'Are you sure you want to synchronize the passwords of this application with the passwords of the Telegram bot?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Синхронізація бази даних',
            'Ви впевнені, що хочете синхронізувати паролі цього додатка з паролями Telegram-бота?'
        )

    return user_choice


def token_input_message(lang_state_check, application_window):
    if lang_state_check:
        user_choice = custom_askstring(
            'Token input', 'Enter the token assigned to you by the bot\n(use /token command in Telegram)...\n',
            parent=application_window, lang_state=lang_state_check
        )
    else:
        user_choice = custom_askstring(
            'Ввід токену',
            'Введіть токен, який присвоїв вам бот\n(використовуйте команду /token у Telegram)...\n',
            parent=application_window, lang_state=lang_state_check
        )

    return user_choice


def input_token_error_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'Invalid input',
            'Token is entered incorrectly or does not exist! Check the correctness of the input or generate it in bot.'
        )
    else:
        messagebox.showwarning(
            'Некоректний ввід',
            'Токен введений невірно або його не існує! Перевірте правильність вводу або згенеруйте його в боті.'
        )


def server_token_changed_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'Token was changed',
            'You have changed the token. Enter a new token.'
        )
    else:
        messagebox.showwarning(
            'Токен було змінено',
            'Ви змінили токен. Введіть новий токен.'
        )


def data_is_identical_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo('Data is up-to-date', 'Data in the bot database and the local database are identical.')
    else:
        messagebox.showinfo('Дані актуальні', 'Дані в базі даних бота та локальній базі ідентичні.')


def error_sync_message(lang_state_check, load_screen):
    load_screen.destroy()

    if lang_state_check:
        messagebox.showerror(
            'Database error',
            'Unexpected error during synchronization.\nCanceling the process...'
        )
    else:
        messagebox.showerror(
            'Помилка бази даних',
            'Неочікувана помилка під час синхронізації. Відміна процесу...'
        )


def successful_sync_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Operation successful!',
            'Passwords have been successfully synchronized. Press "Reload" to see changes.'
        )
    else:
        messagebox.showinfo(
            'Операція успішна!',
            'Паролі успішно синхронізовано. Натисніть "Оновити", щоб побачити зміни.'
        )


def connection_error_message(lang_state_check, load_screen):
    load_screen.destroy()

    if lang_state_check:
        messagebox.showerror(
            'Connection error',
            'Synchronization is not possible due to lack of Internet connection.'
        )
    else:
        messagebox.showerror(
            'Помилка з’єднання',
            'Синхронізація неможлива, через відсутність Інтернет з’єднання.'
        )


def connection_timeout_message(lang_state_check, load_screen):
    load_screen.destroy()

    if lang_state_check:
        messagebox.showerror(
            'Connection timeout',
            'Synchronization is not possible because the waiting time is too long.'
        )
    else:
        messagebox.showerror(
            'Закінчення часу очікування',
            'Синхронізація неможлива, через занадто довгий час очікування.'
        )


def ask_to_save_token_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'Save token', 'Would you like to save this token for future synchronizations?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Збереження токену', 'Ви хочете зберегти цей токен для наступних синхронізацій?'
        )

    return user_choice


def choose_between_duplicates_message(lang_state_check, application_window):
    if lang_state_check:
        user_choice = custom_askstring(
            'Duplicate password description found',
            'Enter "Remote" to keep remote passwords, or enter "Local" to keep local passwords.\n',
            parent=application_window, lang_state=lang_state_check
        )
    else:
        user_choice = custom_askstring(
            'Знайдено дубльований опис пароля',
            'Введіть "Сервер", щоб зберегти паролі з сервера, або введіть "Локально", щоб зберегти локальні паролі',
            parent=application_window, lang_state=lang_state_check
        )

    return user_choice


def show_warn_by_regex_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'Invalid input',
            'You can enter only the word "Server" to save passwords from the server, '
            'or "Local" to save local passwords. It is forbidden to enter any other words.'
        )
    else:
        messagebox.showwarning(
            'Некоректний ввід',
            'Ви можете ввести тільки слово "Сервер", щоб зберегти паролі з сервера, '
            'або "Локально", щоб зберегти локальні паролі. Інші будь-які слова вводити заборонено.',
        )


def ask_to_save_new_token(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'New token',
            'Save this new token for future synchronizations?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Новий токен',
            'Зберегти цей новий токен для наступних синхронізацій?'
        )

    return user_choice


def successfully_changed_token_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Token changed',
            'Token was successfully changed and saved!'
        )
    else:
        messagebox.showinfo(
            'Токен змінено',
            'Токен було успішно змінено і збережено!'
        )


def was_not_changed_token_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo(
            'Token not changed',
            'Token was not changed. Try again to set and save new token.'
        )
    else:
        messagebox.showinfo(
            'Токен не змінено',
            'Токен не було змінено. Спробуйте ще раз, щоб змінити і зберегти новий токен.'
        )


def search_query_input_message(lang_state_check):
    if lang_state_check:
        user_choice = custom_askstring(
            'Search',
            'Enter a search query (a description of the password you want to find).\nSearch is case-insensitive.\n',
            lang_state=lang_state_check
        )
    else:
        user_choice = custom_askstring(
            'Пошук',
            'Введіть пошуковий запит (опис пароля, який хочете знайти).\nПошук є регістро незалежним.\n',
            lang_state=lang_state_check
        )

    return user_choice


def invalid_search_query_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'Invalid search query',
            'Search query cannot be empty space or has more than 384 symbols in it! Try again.'
        )
    else:
        messagebox.showwarning(
            'Некоректний пошуковий запит',
            'Пошуковий запит не можу бути пустим місцем або мати більше ніж 384 символи! Спробуйте ще раз.',
        )


def no_matches_for_search_message(lang_state_check, search_query):
    if lang_state_check:
        messagebox.showinfo(
            'No matches',
            f'No mathes for query:\n{search_query}'
        )
    else:
        messagebox.showinfo(
            'Відсутні збіги',
            f'Збіги відсутні на запит:\n{search_query}',
        )
