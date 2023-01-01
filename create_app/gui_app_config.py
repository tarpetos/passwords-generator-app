import tkinter
from tkinter.constants import TOP, LEFT
from tkinter import ttk
from tkinter.ttk import Label, Entry, Button, Radiobutton, Frame

from change_interface_look.change_background_color import AppBackgroundTheme
from change_interface_look.change_radiobtn_text_position import change_text_pos
from create_app.create_sql_table import TableInterface
from create_app.inputs_and_buttons_processing import generate_password, copy_password, write_to_database, clear_entries, \
    english_language_main_window_data, ukrainian_language_main_window_data, remove_record_from_table, \
    english_language_table_window_data, ukrainian_language_table_window_data, sync_db_data

change_background = AppBackgroundTheme()


class PasswordGeneratorApp(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side=TOP, fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages_tuple = (MainPage, TablePage)

        for page in pages_tuple:
            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky='nswe')

        self.show_frame(MainPage)

        frame_style = ttk.Style()
        frame_style.configure('TFrame', background='black')

        scrollbar_frame_style = ttk.Style()
        scrollbar_frame_style.configure('ScrolledFrame', background='black')

        button_style = ttk.Style()
        button_style.configure(
            'TButton',
            background='#00D8A1',
            font=('Arial Black', 8, 'bold')
        )

        change_bg_style = ttk.Style()
        change_bg_style.configure('BG.TButton', font=('Arial', 9))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        main_frame = Frame(self)

        password_usage_label = Label(
            main_frame,
            text='For what this password should be?:',
            font='Arial 8 bold',
            # foreground='white',
            # background='black,'
        )
        password_length_label = Label(
            main_frame,
            text='Enter password length:',
            font='Arial 8 bold'
        )
        repeatable_label = Label(
            main_frame,
            text='Can be repeatable characters in password(y/n)?:',
            font='Arial 8 bold'
        )
        result_password_label = Label(
            main_frame,
            text='GENERATED PASSWORD',
            font='Arial 8 bold'
        )

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
            takefocus=0,
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
            padding=8,
        )

        copy_btn = Button(
            main_frame,
            text='Copy password',
            command=lambda: copy_password(result_password_entry),
            padding=8,
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
            padding=8,
        )

        write_to_db_btn = Button(
            main_frame,
            text='Write to database',
            command=lambda:
                write_to_database(
                    password_usage_entry.get(),
                    result_password_entry.get()
                ),
            padding=8,
        )

        quit_btn = Button(
            main_frame,
            text='Quit',
            command=lambda: app.destroy(),
            padding=8
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
            padding=8,
            style='BG.TButton'
        )

        change_bg_btn.invoke()

        move_to_table_btn = ttk.Button(
            main_frame,
            text='Show table >>>>',
            padding=8,
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
            padding=8,
        )

        ukrainian_lang = Button(
            main_frame,
            text='UA',
            command=lambda: ukrainian_language_main_window_data(
                labels_dict,
                buttons_dict,
                radiobtn_dict,
            ),
            padding=8
        )

        password_usage_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 10))
        password_usage_entry.grid(row=0, column=3, columnspan=3, sticky='e', pady=(0, 10))

        password_length_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=10)
        password_length_entry.grid(row=1, column=3, columnspan=3, sticky='e', pady=10)

        repeatable_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=10)
        repeatable_entry.grid(row=2, column=3, columnspan=3, sticky='e', pady=10)

        generate_btn.grid(row=3, column=0, columnspan=3, sticky='we', padx=(0, 2), pady=20)
        ukrainian_lang.grid(row=3, column=3, sticky='we', padx=(2, 2))
        change_bg_btn.grid(row=3, column=4, sticky='we', padx=(2, 2))
        english_lang.grid(row=3, column=5, sticky='we', padx=(2, 0))

        all_symbols.grid(row=4, column=0)
        only_letters.grid(row=4, column=1)
        only_digits.grid(row=4, column=2)
        letters_digits.grid(row=4, column=3)
        letters_signs.grid(row=4, column=4,)
        digits_signs.grid(row=4, column=5)

        result_password_label.grid(row=5, column=0, pady=(45, 0), columnspan=6)
        result_password_entry.grid(row=6, column=0, sticky='nswe', pady=10, columnspan=6)

        copy_btn.grid(row=7, column=0, columnspan=2, sticky='we', pady=20, padx=(0, 2))
        clear_btn.grid(row=7, column=2, columnspan=2, sticky='we', pady=20, padx=(2, 2))
        write_to_db_btn.grid(row=7, column=4, columnspan=2, sticky='we', pady=20, padx=(2, 0))

        quit_btn.grid(row=8, column=0, columnspan=3, sticky='we', padx=(0, 2))
        move_to_table_btn.grid(row=8, column=3, columnspan=3, sticky='we', padx=(2, 0))

        main_frame.pack(side=TOP, pady=50)


class TablePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        full_frame = Frame(self)

        table_page_frame = Frame(full_frame)

        table_frame = Frame(table_page_frame)
        all_data_from_table = TableInterface(table_frame)
        all_data_from_table.get_data_from_table()

        return_to_main_btn = Button(
            table_page_frame,
            text='<<<< Back',
            padding=8,
            command=lambda: controller.show_frame(MainPage)
        )

        reload_table_btn = Button(
            table_page_frame,
            text='Reload',
            padding=8,
            command=lambda: [
                all_data_from_table.get_data_from_table(),
            ]
        )

        update_table_btn = Button(
            table_page_frame,
            text='Update',
            padding=8,
            command=lambda: [
                all_data_from_table.update_data_using_table_interface()
            ]
        )

        delete_record_btn = Button(
            table_page_frame,
            text='Delete',
            padding=8,
            command=lambda: [
                remove_record_from_table(app),
                all_data_from_table.get_data_from_table()
            ]
        )

        synchronize_data = Button(
            table_page_frame,
            text='Synchronize password data',
            command=lambda: [
                sync_db_data(app),
            ],
            padding=8,
            # style='BG.TButton'
        )

        quit_btn = Button(
            table_page_frame,
            text='Quit',
            padding=8,
            command=lambda: app.destroy(),
        )


        table_buttons_dict = {
            'synchronize_data': synchronize_data,
            'return_to_main_btn': return_to_main_btn,
            'reload_table_btn': reload_table_btn,
            'update_table_btn': update_table_btn,
            'delete_record_btn': delete_record_btn,
            'table_quit_btn': quit_btn,
        }

        # change_bg_btn.invoke()

        english_lang = Button(
            table_page_frame,
            text='EN',
            command=lambda: [
                english_language_table_window_data(table_buttons_dict),
                all_data_from_table.get_data_from_table()
            ],
            padding=8,
        )

        ukrainian_lang = Button(
            table_page_frame,
            text='UA',
            command=lambda: [
                ukrainian_language_table_window_data(table_buttons_dict),
                all_data_from_table.get_data_from_table()
            ],
            padding=8,
        )

        ukrainian_lang.grid(row=0, column=0, sticky='we', padx=(0, 2))
        synchronize_data.grid(row=0, column=1, columnspan=3, sticky='we', padx=(2, 2))
        english_lang.grid(row=0, column=4, columnspan=2, sticky='we', padx=(2, 0))
        table_frame.grid(row=1, column=0, columnspan=5, sticky='nswe', pady=5)
        return_to_main_btn.grid(row=2, column=0, sticky='we', padx=(0, 2))
        reload_table_btn.grid(row=2, column=1, sticky='we', padx=(2, 2))
        update_table_btn.grid(row=2, column=2, sticky='we', padx=(2, 2))
        delete_record_btn.grid(row=2, column=3, sticky='we', padx=(2, 2))
        quit_btn.grid(row=2, column=4, sticky='we', padx=(2, 0))
        table_page_frame.pack(side=LEFT)
        full_frame.pack(side=TOP, pady=15)
    

app = PasswordGeneratorApp()
