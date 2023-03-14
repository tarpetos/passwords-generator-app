from tkinter import messagebox

from customtkinter import CTkInputDialog


def invalid_password_description_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Length of password usage field have to be in range from 1 to 500!')
    else:
        messagebox.showerror(
            'Некоректний ввід',
            'Кількість символів в полі призначення має знаходитись в межах від 1 до 500!'
        )


def invalid_password_type_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Password length should be integer number!')
    else:
        messagebox.showerror('Некоректний ввід', 'Значення довжини пароля повинно бути цілим числом!')


def invalid_password_value_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Length of password have to be in range from 1 to 500')
    else:
        messagebox.showerror('Некоректний ввід', 'Значення довжини має знаходитись в межах від 1 до 500!')


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


def invalid_value_for_repeatable_or_not_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror(
            'Invalid input',
            'You can use only "y/Y" or "n/N" to allow or to not allow repeatable characters!'
        )
    else:
        messagebox.showerror(
            'Некоректний ввід',
            'Ви можете використовувати тільки "т/Т" або "н/Н", щоб дозволити чи заборонити повторювані символи!'
        )


def empty_result_input_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror(
            'Field is unfilled',
            'No password in result field!!!\nGenerate or type it and then write to database.'
        )
    else:
        messagebox.showerror(
            'Незаповнене поле',
            'Пароль відсутній!!!\n'
            'Згенеруйте або введіть його і тоді запишіть до бази даних.'
        )


def ask_write_to_database_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'Writing to database...',
            'Would you like to write this data to database?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Запис до бази даних...',
            'Ви хочете записати дані до бази даних?'
        )

    return user_choice


def ask_if_record_exist_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno(
            'Accept or decline writing...',
            'A record with such description already exists.\n'
            'Are you sure you want to change the password associated with this record?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Прийняти або відхилити записування...',
            'Запис з таким описом вже існує.\n'
            'Ви впевнені, що хочете змінити пароль, який відноситься до цього запису?'
        )

    return user_choice


def successful_write_to_database_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo('Database info', 'All password data was written to database!')
    else:
        messagebox.showinfo('Інформація про базу даних', 'Дані успішно записано до бази даних!')


def unexpected_database_error_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Database error', 'Unexpected error while writing to database!')
    else:
        messagebox.showerror('Помилка бази даних', 'Неочікувана помилка під час запису даних до бази!')


def nothing_to_copy_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning('Copy', 'Nothing to copy!')
    else:
        messagebox.showwarning('Копіювання', 'Дані для копіювання відсутні!')


def copy_successful_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo('Copy', 'Data from password text box was copied to clipboard!')
    else:
        messagebox.showinfo('Копіювання', 'Пароль успішно був скопійований до буфера обміну!')


def clear_all_fields_message(lang_state_check):
    if lang_state_check:
        messagebox.showinfo('Clear', 'Data from all fields were cleared!')
    else:
        messagebox.showinfo('Очищення', 'Дані з всіх полів були очищені успішно!')


def empty_table_warn(lang_state_check):
    if lang_state_check:
        messagebox.showwarning('Empty table', 'There are no records in the local table!')
    else:
        messagebox.showwarning('таблиця пуста', 'У локальній таблиці немає записів!')


def input_dialog_message(lang_state_check):
    if lang_state_check:
        user_input_choice = CTkInputDialog(
            title='ID input', text='Enter the ID of the record you want to delete...',
        )
    else:
        user_input_choice = CTkInputDialog(
            title='Ввід ID', text='Введіть ID запису, який ви хочете видалити...',
        )

    return user_input_choice.get_input()


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
        )
    else:
        messagebox.showinfo(
            'Зміна таблиці',
            'Ви змінили дані в таблиці! Зміни записано успішно.\n'
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
            'Are you sure you want to synchronize the passwords of '
            'this application with the passwords of the Telegram bot?'
        )
    else:
        user_choice = messagebox.askyesno(
            'Синхронізація бази даних',
            'Ви впевнені, що хочете синхронізувати паролі цього додатка з паролями Telegram-бота?'
        )

    return user_choice


def token_input_message(lang_state_check):
    if lang_state_check:
        user_choice = CTkInputDialog(
            title='Token input',
            text='Enter the token assigned to you by the bot\n(use /token command in Telegram)...\n',
        )
    else:
        user_choice = CTkInputDialog(
            title='Ввід токену',
            text='Введіть токен, який присвоїв вам бот\n(використовуйте команду /token у Telegram)...\n',
        )

    return user_choice.get_input()


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


def choose_between_duplicates_message(lang_state_check):
    if lang_state_check:
        user_choice = CTkInputDialog(
            title='Duplicate password description found',
            text='Enter "Remote" to keep remote passwords, or enter "Local" to keep local passwords.\n',
        )
    else:
        user_choice = CTkInputDialog(
            title='Знайдено дубльований опис пароля',
            text='Введіть "Сервер", щоб зберегти паролі з сервера, '
                 'або введіть "Локально", щоб зберегти локальні паролі',
        )

    return user_choice.get_input()


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
        user_choice = CTkInputDialog(
            title='Search',
            text='Enter a search query (description of the password you want to find).\nSearch is case-insensitive.\n',
        )
    else:
        user_choice = CTkInputDialog(
            title='Пошук',
            text='Введіть пошуковий запит (опис пароля, який хочете знайти).\nПошук є регістро незалежним.\n',
        )

    return user_choice.get_input()


def invalid_search_query_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning(
            'Invalid search query',
            'Search query cannot be empty space or has more than 500 symbols in it! Try again.'
        )
    else:
        messagebox.showwarning(
            'Некоректний пошуковий запит',
            'Пошуковий запит не можу бути пустим місцем або мати більше ніж 500 символів! Спробуйте ще раз.',
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
