import tkinter
from tkinter.constants import TOP
from tkinter.ttk import Label, Entry, Button

from modules.change_background_color import ChangeAppBackgroundTheme
from modules.inputs_and_buttons_validation import generate_password, copy_password, clear_entries, \
     english_language_main_window_data, ukrainian_language_main_window_data


def make_window():
    root = tkinter.Tk()
    root.title('Password Generator')
    root.geometry('700x500')
    frame = tkinter.Frame(root)
    frame.grid()

    password_usage_label = Label(frame, text='For what this password should be?:', font='Aerial 9 bold')
    password_length_label = Label(frame, text='Enter password length:', font='Aerial 9 bold')
    repeatable_label = Label(frame, text='Can be repeatable characters in password(y/n)?:', font='Aerial 9 bold')
    result_password_label = Label(frame, text='GENERATED PASSWORD', font='Aerial 9 bold')

    password_usage_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
    password_length_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
    repeatable_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
    result_password_label.grid(row=4, column=0, pady=5, padx=10, columnspan=2)

    password_usage_entry = Entry(frame, width=50)
    password_length_entry = Entry(frame, width=50)
    repeatable_entry = Entry(frame, width=50)
    result_password_entry = Entry(frame)

    password_usage_entry.grid(row=0, column=1, pady=10)
    password_length_entry.grid(row=1, column=1, pady=10)
    repeatable_entry.grid(row=2, column=1, pady=10)
    result_password_entry.grid(row=5, column=0, sticky='nesw', pady=10, columnspan=2)

    generate_btn = Button(
        frame,
        text='Generate',
        command=lambda: generate_password(
            password_usage_entry,
            password_length_entry,
            repeatable_entry,
            result_password_entry
        ),
        padding=10
    )

    quit_btn = Button(
        frame, text='Quit',
        command=root.destroy,
        padding=10
    )

    copy_btn = Button(
        frame,
        text='Copy password',
        command=lambda: copy_password(result_password_entry),
        padding=10
    )

    clear_btn = Button(
        frame,
        text='Clear all',
        command=lambda:
            clear_entries(
                password_usage_entry,
                password_length_entry,
                repeatable_entry,
                result_password_entry
            ),
        padding=10,
    )

    labels_dict = {
        'password_usage_label': password_usage_label,
        'password_length_label': password_length_label,
        'repeatable_label': repeatable_label,
        'result_password_label': result_password_label
    }

    change_background = ChangeAppBackgroundTheme()

    change_bg_btn = Button(
        frame,
        text=u'\u263C',
        command=lambda:
            change_background.change_background_color(
                root,
                frame,
                labels_dict,
                change_bg_btn
            ),
        padding=10
    )

    buttons_dict = {
        'generate_btn': generate_btn,
        'quit_btn': quit_btn,
        'copy_btn': copy_btn,
        'clear_btn': clear_btn
    }

    english_lang = Button(
        frame,
        text='EN',
        command=lambda: english_language_main_window_data(labels_dict, buttons_dict),
        padding=10
    )

    ukrainian_lang = Button(
        frame,
        text='UA',
        command=lambda: ukrainian_language_main_window_data(labels_dict, buttons_dict),
        padding=10
    )

    generate_btn.grid(row=3, column=0, sticky='nesw', pady=20)
    quit_btn.grid(row=3, column=1, sticky='nesw', pady=20)
    copy_btn.grid(row=6, column=0, sticky='nesw', pady=20)
    clear_btn.grid(row=6, column=1, sticky='nesw', pady=20)

    ukrainian_lang.grid(row=7, column=0, sticky='w')
    english_lang.grid(row=7, column=0)
    change_bg_btn.grid(row=7, column=0, sticky='e')

    frame.pack(side=TOP, padx=10, pady=40)
    root.resizable(False, False)
    root.mainloop()
