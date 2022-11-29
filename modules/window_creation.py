import tkinter
from tkinter.constants import TOP
from tkinter.ttk import Label, Entry, Button, Radiobutton

from modules.change_background_color import ChangeAppBackgroundTheme
from modules.change_radiobtn_text_position import change_text_pos
from modules.inputs_and_buttons_validation import generate_password, copy_password, clear_entries, \
    english_language_main_window_data, ukrainian_language_main_window_data, write_to_database


def make_window():
    root = tkinter.Tk()
    root.title('Password Generator')
    root.geometry('700x540')
    frame = tkinter.Frame(root)
    frame.grid()

    password_usage_label = Label(frame, text='For what this password should be?:', font='Aerial 9 bold')
    password_length_label = Label(frame, text='Enter password length:', font='Aerial 9 bold')
    repeatable_label = Label(frame, text='Can be repeatable characters in password(y/n)?:', font='Aerial 9 bold')
    result_password_label = Label(frame, text='GENERATED PASSWORD', font='Aerial 9 bold')

    password_usage_entry = Entry(frame, width=50)
    password_length_entry = Entry(frame, width=50)
    repeatable_entry = Entry(frame, width=50)
    result_password_entry = Entry(frame)

    change_text_pos()  # set bottom text position in radiobuttons

    radiobutton_choice_option = tkinter.IntVar()
    radiobutton_choice_option.set(1)  # default option is all symbols

    all_symbols = Radiobutton(frame, text='All symbols', variable=radiobutton_choice_option, value=1, takefocus=0)
    only_letters = Radiobutton(frame, text='Only letters', variable=radiobutton_choice_option, value=2, takefocus=0)
    only_digits = Radiobutton(frame, text='Only digits', variable=radiobutton_choice_option, value=3, takefocus=0)
    letters_digits = Radiobutton(frame, text='Letters & digits', variable=radiobutton_choice_option, value=4,
                                 takefocus=0)
    letters_signs = Radiobutton(frame, text='Letters & signs', variable=radiobutton_choice_option, value=5, takefocus=0)
    digits_signs = Radiobutton(frame, text='Digits & signs', variable=radiobutton_choice_option, value=6, takefocus=0)

    radiobtn_dict = {
        'all_symbols': all_symbols,
        'only_letters': only_letters,
        'only_digits': only_digits,
        'letters_digits': letters_digits,
        'letters_signs': letters_signs,
        'digits_signs': digits_signs,
    }

    generate_btn = Button(
        frame,
        text='Generate',
        command=lambda: generate_password(
            password_usage_entry,
            password_length_entry,
            repeatable_entry,
            result_password_entry,
            radiobutton_choice_option
        ),
        padding=10
    )

    copy_btn = Button(
        frame,
        text='Copy password',
        command=lambda: copy_password(result_password_entry),
        padding=10,
        width=29
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
        width=28
    )

    write_to_db_btn = Button(
        frame,
        text='Write to database',
        command=lambda: write_to_database(
            password_usage_entry.get(),
            password_length_entry.get(),
            result_password_entry.get()
        ),
        padding=10,
        width=29
    )

    quit_btn = Button(
        frame, text='Quit',
        command=root.destroy,
        padding=10
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
            change_bg_btn,
            radiobtn_dict,
        ),
        padding=10,
        width=14
    )

    buttons_dict = {
        'generate_btn': generate_btn,
        'copy_btn': copy_btn,
        'clear_btn': clear_btn,
        'write_to_db_btn': write_to_db_btn,
        'quit_btn': quit_btn,
    }

    english_lang = Button(
        frame,
        text='EN',
        command=lambda: english_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict),
        padding=10,
    )

    ukrainian_lang = Button(
        frame,
        text='UA',
        command=lambda: ukrainian_language_main_window_data(labels_dict, buttons_dict, radiobtn_dict),
        padding=10
    )

    password_usage_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
    password_usage_entry.grid(row=0, column=1, pady=10)

    password_length_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
    password_length_entry.grid(row=1, column=1, pady=10)

    repeatable_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
    repeatable_entry.grid(row=2, column=1, pady=10)

    generate_btn.grid(row=3, column=0, sticky='we', padx=(0, 2), pady=20)
    ukrainian_lang.grid(row=3, column=1, sticky='w', padx=(1, 0))
    change_bg_btn.grid(row=3, column=1, padx=(3, 2))
    english_lang.grid(row=3, column=1, sticky='e')

    all_symbols.grid(row=4, column=0, sticky='w')
    only_letters.grid(row=4, column=0)
    only_digits.grid(row=4, column=0, sticky='e', padx=(0, 15))
    letters_digits.grid(row=4, column=1, sticky='w', padx=(15, 0))
    letters_signs.grid(row=4, column=1)
    digits_signs.grid(row=4, column=1, sticky='e')

    result_password_label.grid(row=5, column=0, pady=(30, 0), padx=10, columnspan=2)
    result_password_entry.grid(row=6, column=0, sticky='nesw', pady=10, columnspan=2)

    copy_btn.grid(row=7, column=0, columnspan=2, sticky='w', pady=20)
    clear_btn.grid(row=7, column=0, columnspan=2, pady=20)
    write_to_db_btn.grid(row=7, column=0, columnspan=2, sticky='e', pady=20)

    quit_btn.grid(row=8, column=0, sticky='we', padx=150, columnspan=2)

    frame.pack(side=TOP, padx=10, pady=40)
    root.resizable(False, False)
    root.mainloop()
