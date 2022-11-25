from tkinter import messagebox


def ivalid_password_usage_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Length of password usage field have to be in range from 1 to 384!')
    else:
        messagebox.showerror('Некоректний ввід',
                             'Кількість символів в полі призначення має знаходитись в межах від 1 до 384!')


def invalid_password_type_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Password length should be integer number!')
    else:
        messagebox.showerror('Некоректний ввід', 'Значення довжини пароля повинно бути цілим числом!')


def invalid_password_value_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Length of password have to be in range from 1 to 384')
    else:
        messagebox.showerror('Некоректний ввід', 'Значення довжини має знаходитись в межах від 1 до 384!')


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
            'Ви можете використовувати тільки "y/Y" або "n/N", щоб дозволити чи заборонити повторювані символи!'
        )


def ask_write_to_database_message(lang_state_check):
    if lang_state_check:
        user_choice = messagebox.askyesno('Writing to database...',
                                          'Would you like to write this data to database?')
    else:
        user_choice = messagebox.askyesno('Запис до бази даних...',
                                          'Ви хочете записати дані до бази даних?')

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
