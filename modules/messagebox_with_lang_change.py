from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import Dialog


def ivalid_password_usage_message(lang_state_check):
    if lang_state_check:
        messagebox.showerror('Invalid input', 'Length of password usage field have to be in range from 1 to 384!')
    else:
        messagebox.showerror(
            'Некоректний ввід',
            'Кількість символів в полі призначення має знаходитись в межах від 1 до 384!'
        )


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
        user_choice = messagebox.askyesno('Writing to database...', 'Would you like to write this data to database?')
    else:
        user_choice = messagebox.askyesno('Запис до бази даних...', 'Ви хочете записати дані до бази даних?')

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


def input_dialog_message(lang_state_check, application_window):
    class _CustomDialog(Dialog):
        def __init__(self, title, prompt, initialvalue=None, parent=None):
            self.prompt = prompt

            self.initialvalue = initialvalue

            Dialog.__init__(self, parent, title)

        def destroy(self):
            self.entry = None
            Dialog.destroy(self)

        def body(self, master):

            w = Label(master, text=self.prompt, justify=LEFT)
            w.grid(row=0, padx=5, sticky=W)

            self.entry = Entry(master, name="entry")
            self.entry.grid(row=1, padx=5, sticky=W + E)

            if self.initialvalue is not None:
                self.entry.insert(0, self.initialvalue)
                self.entry.select_range(0, END)

            return self.entry

        def validate(self):
            try:
                result = self.getresult()
            except ValueError:
                if lang_state_check:
                    messagebox.showwarning(
                        "Invalid input",
                        "Not an integer! Try again.",
                        parent=self
                    )
                else:
                    messagebox.showwarning(
                        "Некоректний ввід",
                        "Введено не ціле число! Спробуйте ще раз.",
                        parent=self
                    )
                return 0

            self.result = result

            return 1

    class _QueryInteger(_CustomDialog):
        def getresult(self):
            return self.getint(self.entry.get())

    def askinteger(title, prompt, **kw):
        d = _QueryInteger(title, prompt, **kw)
        return d.result

    if lang_state_check:
        user_input_choice = askinteger(
            'ID input', 'Enter the ID of the record you want to delete...', parent=application_window
        )
    else:
        user_input_choice = askinteger(
            'Ввід ID', 'Введіть ID запису, який ви хочете видалити...', parent=application_window
        )

    return user_input_choice


def input_dialog_error_message(lang_state_check):
    if lang_state_check:
        messagebox.showwarning('Invalid input', 'No ID with such value in the table! Try again.')
    else:
        messagebox.showwarning('Некоректний ввід', 'ID таким значенням відсутній у таблиці. Спробуйте ще раз.')


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
            'You have changed the data in the table! Changes saved successfully.\n'
            'Reload the table to reflect the changes.'
        )
    else:
        messagebox.showinfo(
            'Зміна таблиці',
            'Ви змінили дані в таблиці! Зміни записано успішно.\n'
            'Оновіть таблицю для відображення змін.'
        )
