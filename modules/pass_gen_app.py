import tkinter
from tkinter.constants import TOP, LEFT
from tkinter import ttk
from tkinter.ttk import Label, Entry, Button, Radiobutton

from modules.change_background_color import ChangeAppBackgroundTheme
from modules.change_radiobtn_text_position import change_text_pos
from modules.create_sql_table import CreateTable
from modules.inputs_and_buttons_validation import generate_password, copy_password, clear_entries, \
    english_language_main_window_data, ukrainian_language_main_window_data, write_to_database, \
    english_language_table_window_data, ukrainian_language_table_window_data

change_background = ChangeAppBackgroundTheme()


class PasswordGeneratorApp(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        container = tkinter.Frame(self)
        container.pack(side=TOP, fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages_tuple = (MainPage, TablePage)

        for page in pages_tuple:
            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nesw")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        main_frame = tkinter.Frame(self)

        password_usage_label = Label(main_frame, text='For what this password should be?:', font='Aerial 9 bold')
        password_length_label = Label(main_frame, text='Enter password length:', font='Aerial 9 bold')
        repeatable_label = Label(main_frame, text='Can be repeatable characters in password(y/n)?:',
                                 font='Aerial 9 bold')
        result_password_label = Label(main_frame, text='GENERATED PASSWORD', font='Aerial 9 bold')

        password_usage_entry = Entry(main_frame, width=50)
        password_length_entry = Entry(main_frame, width=50)
        repeatable_entry = Entry(main_frame, width=50)
        result_password_entry = Entry(main_frame)

        change_text_pos()  # set bottom text position in radiobuttons

        radiobutton_choice_option = tkinter.IntVar()
        radiobutton_choice_option.set(1)  # default option is all symbols

        all_symbols = Radiobutton(
            main_frame,
            text='All symbols',
            variable=radiobutton_choice_option,
            value=1,
            takefocus=0
        )
        only_letters = Radiobutton(
            main_frame,
            text='Only letters',
            variable=radiobutton_choice_option,
            value=2,
            takefocus=0
        )
        only_digits = Radiobutton(
            main_frame,
            text='Only digits',
            variable=radiobutton_choice_option,
            value=3,
            takefocus=0
        )
        letters_digits = Radiobutton(
            main_frame,
            text='Letters & digits',
            variable=radiobutton_choice_option,
            value=4,
            takefocus=0
        )
        letters_signs = Radiobutton(
            main_frame,
            text='Letters & signs',
            variable=radiobutton_choice_option,
            value=5,
            takefocus=0
        )
        digits_signs = Radiobutton(
            main_frame,
            text='Digits & signs',
            variable=radiobutton_choice_option,
            value=6,
            takefocus=0
        )

        radiobtn_dict = {
            'all_symbols': all_symbols,
            'only_letters': only_letters,
            'only_digits': only_digits,
            'letters_digits': letters_digits,
            'letters_signs': letters_signs,
            'digits_signs': digits_signs,
        }

        generate_btn = Button(
            main_frame,
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
            main_frame,
            text='Copy password',
            command=lambda: copy_password(result_password_entry),
            padding=10,
            width=28
        )

        clear_btn = Button(
            main_frame,
            text='Clear all',
            command=lambda:
            clear_entries(
                password_usage_entry,
                password_length_entry,
                repeatable_entry,
                result_password_entry
            ),
            padding=10,
            width=27
        )

        write_to_db_btn = Button(
            main_frame,
            text='Write to database',
            command=lambda: write_to_database(
                password_usage_entry.get(),
                password_length_entry.get(),
                result_password_entry.get()
            ),
            padding=10,
            width=28
        )

        quit_btn = Button(
            main_frame,
            text='Quit',
            command=lambda: app.destroy(),
            padding=10
        )

        labels_dict = {
            'password_usage_label': password_usage_label,
            'password_length_label': password_length_label,
            'repeatable_label': repeatable_label,
            'result_password_label': result_password_label
        }

        change_bg_btn = Button(
            main_frame,
            text=u'\u263C',
            command=lambda: [
                change_background.change_background_color(
                    self,
                    main_frame,
                    labels_dict,
                    change_bg_btn,
                    radiobtn_dict,
                ),
            ],
            padding=10,
            width=14
        )

        move_to_table_btn = ttk.Button(
            main_frame,
            text="Show table >>>>",
            padding=10,
            command=lambda: controller.show_frame(TablePage)
        )

        buttons_dict = {
            'generate_btn': generate_btn,
            'copy_btn': copy_btn,
            'clear_btn': clear_btn,
            'write_to_db_btn': write_to_db_btn,
            'move_to_table_btn': move_to_table_btn,
            'quit_btn': quit_btn,
        }

        english_lang = Button(
            main_frame,
            text='EN',
            command=lambda: english_language_main_window_data(
                labels_dict,
                buttons_dict,
                radiobtn_dict,
            ),
            padding=10,
        )

        ukrainian_lang = Button(
            main_frame,
            text='UA',
            command=lambda: ukrainian_language_main_window_data(
                labels_dict,
                buttons_dict,
                radiobtn_dict,
            ),
            padding=10
        )

        password_usage_label.grid(row=0, column=0, sticky='w', pady=(50, 10), padx=(0, 2))
        password_usage_entry.grid(row=0, column=1, pady=(50, 10), padx=(1, 0))

        password_length_label.grid(row=1, column=0, sticky='w', pady=10, padx=(0, 2))
        password_length_entry.grid(row=1, column=1, pady=10, padx=(1, 0))

        repeatable_label.grid(row=2, column=0, sticky='w', pady=10, padx=(0, 2))
        repeatable_entry.grid(row=2, column=1, pady=10, padx=(1, 0))

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

        quit_btn.grid(row=8, column=0, sticky='we', padx=(0, 2))
        move_to_table_btn.grid(row=8, column=1, sticky='we', padx=(1, 0))

        main_frame.pack(side=TOP)


class TablePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        full_frame = tkinter.Frame(self)

        table_page_frame = tkinter.Frame(full_frame)

        table_frame = tkinter.Frame(table_page_frame)
        all_data_from_table = CreateTable(table_frame)
        all_data_from_table.get_data_from_table()

        return_to_main_btn = Button(
            table_page_frame,
            text='<<<< Back',
            width=32,
            padding=10,
            command=lambda: controller.show_frame(MainPage)
        )

        reload_table_btn = Button(
            table_page_frame,
            text='Reload table',
            width=31,
            padding=10,
            command=lambda: all_data_from_table.get_data_from_table()
        )

        quit_btn = Button(
            table_page_frame,
            text='Quit',
            width=32,
            padding=10,
            command=lambda: app.destroy(),
        )

        table_buttons_dict = {
            'return_to_main_btn': return_to_main_btn,
            'reload_table_btn': reload_table_btn,
            'table_quit_btn': quit_btn,
        }

        change_bg_btn = Button(
            table_page_frame,
            text=u'\u263C',
            command=lambda: [
                change_background.change_table_page_background_color(
                    self,
                    table_page_frame,
                    change_bg_btn,
                ),
            ],
            padding=10,
            width=32,
        )

        english_lang = Button(
            table_page_frame,
            text='EN',
            command=lambda: english_language_table_window_data(table_buttons_dict),
            padding=10,
            width=31,
        )

        ukrainian_lang = Button(
            table_page_frame,
            text='UA',
            command=lambda: ukrainian_language_table_window_data(table_buttons_dict),
            padding=10,
            width=32,
        )

        ukrainian_lang.grid(row=0, column=0, columnspan=2, sticky='w', pady=(15, 3))
        change_bg_btn.grid(row=0, column=0, columnspan=2, padx=(6, 0), pady=(15, 3))
        english_lang.grid(row=0, column=0, columnspan=2, sticky='e', pady=(15, 3))
        table_frame.grid(row=1, columnspan=2, sticky='nswe', pady=(0, 3))
        return_to_main_btn.grid(row=2, column=0, columnspan=2, sticky='w')
        reload_table_btn.grid(row=2, column=0, columnspan=2, padx=(1, 0))
        quit_btn.grid(row=2, column=0, columnspan=2, sticky='e')
        table_page_frame.pack(side=LEFT)
        full_frame.pack(side=TOP)


app = PasswordGeneratorApp()
