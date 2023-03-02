from tkinter.constants import TOP

import customtkinter
from customtkinter import CTkLabel, CTkButton, CTkRadioButton, CTkFrame, CTkEntry

from app_translation.load_data_for_localization import all_json_localization_data
from change_interface_look.change_background_color import change_background_color, change_messagebox_color
from create_app.create_sql_table import TableInterface
from create_app.inputs_and_buttons_processing import generate_password, copy_password, write_to_database, \
    clear_entries, remove_record_from_table, \
    sync_db_data, change_local_token, \
    database_search, update_columns_via_app_interface


class PasswordGeneratorApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        container = CTkFrame(self)
        container.pack(side=TOP, fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        main_page = MainPage(container, self)
        table_page = TablePage(container, self)

        self.frames[MainPage] = main_page
        self.frames[TablePage] = table_page

        main_page.grid(row=0, column=0, sticky='nsew')
        table_page.grid(row=0, column=0, sticky='nsew')

        self.current_language = True

        self.show_frame(MainPage)

    # @staticmethod
    # def shortcut_search(event):
    #     current_lang = app.current_language
    #     print(current_lang)
    #     database_search(event, current_lang, app)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_language(self, language):
        for frame in self.frames.values():
            if isinstance(frame, BasePage):
                self.current_language = frame.change_language(language)


class BasePage(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.current_language_state_bool = True
        self._current_language_state_str = 'EN'
        self.language_options = all_json_localization_data  # get data for app localization
        customtkinter.set_default_color_theme('green')  # set default app theme
        change_messagebox_color()  # set default bg and font color to messageboxes

    @staticmethod
    def make_language_state_boolean(language):
        return True if language == 'EN' else False

    def check_if_app_has_element_type(self, element_type, new_data_text):
        if hasattr(self, element_type):
            button = getattr(self, element_type)
            button.configure(text=new_data_text)

    def parse_localization_json_data(self, options):
        for element_group, group_options in options.items():
            for specific_element, text in group_options.items():
                self.check_if_app_has_element_type(specific_element, text)

    def change_language(self, language):
        self.current_language_state_bool = self.make_language_state_boolean(language)
        if language in self.language_options and self._current_language_state_str != language:
            self._current_language_state_str = language
            options = self.language_options[language]
            self.parse_localization_json_data(options)

        return self.current_language_state_bool


class MainPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)

        main_frame = CTkFrame(self)

        self.password_usage_label = CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['password_usage_label']
        )
        self.password_length_label = CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['password_length_label'],
        )
        self.repeatable_label = CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['repeatable_label'],
        )
        self.result_password_label = CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['result_password_label'],
        )

        self.password_usage_entry = CTkEntry(main_frame)
        self.password_length_entry = CTkEntry(main_frame)
        self.repeatable_entry = CTkEntry(main_frame)
        self.result_password_entry = CTkEntry(main_frame)

        radiobutton_choice_option = customtkinter.IntVar()
        radiobutton_choice_option.set(1)  # default option is all symbols

        radiobutton_frame = CTkFrame(main_frame)

        self.all_symbols_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=1,
        )
        self.only_letters_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=2,
        )
        self.only_digits_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=3,
        )
        self.letters_digits_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=4,
        )
        self.letters_signs_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=5,
        )
        self.digits_signs_radio_btn = CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=6,

        )

        self.all_symbols_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['all_symbols_label']
        )
        self.only_letters_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['only_letters_label']
        )
        self.only_digits_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['only_digits_label']
        )
        self.letters_digits_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['letters_digits_label']
        )
        self.letters_signs_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['letters_signs_label']
        )
        self.digits_signs_label = CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['digits_signs_label']
        )

        self.generate_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['generate_btn'],
            text_color='black',
            command=lambda: generate_password(
                self.current_language_state_bool,
                self.password_usage_entry,
                self.password_length_entry,
                self.repeatable_entry,
                self.result_password_entry,
                radiobutton_choice_option
            ),
        )

        self.copy_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['generate_btn'],
            text_color='black',
            command=lambda: copy_password(self.current_language_state_bool, self.result_password_entry),
        )

        self.clear_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['clear_btn'],
            text_color='black',
            command=lambda: clear_entries(
                self.password_usage_entry,
                self.password_length_entry,
                self.repeatable_entry,
                self.result_password_entry
            ),
        )

        self.write_to_db_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['write_to_db_btn'],
            text_color='black',
            command=lambda: write_to_database(
                self.current_language_state_bool,
                self.password_usage_entry.get(),
                self.result_password_entry.get()
            ),
        )

        self.change_bg_btn = CTkButton(
            main_frame,
            text=u'\u263E',
            text_color='black',
            command=lambda: change_background_color(self.change_bg_btn),
        )

        self.move_to_table_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['move_to_table_btn'],
            text_color='black',
            command=lambda: controller.show_frame(TablePage),
        )

        self.ukrainian_lang_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['ukrainian_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('UA'),
        )

        self.english_lang_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['english_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('EN')
        )

        self.quit_btn = CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['quit_btn'],
            text_color='black',
            command=lambda: app.destroy(),
        )

        self.password_usage_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(30, 10), padx=15)
        self.password_usage_entry.grid(row=0, column=3, columnspan=3, sticky='we', pady=(30, 10), padx=(0, 15))

        self.password_length_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=10, padx=15)
        self.password_length_entry.grid(row=1, column=3, columnspan=3, sticky='we', pady=10, padx=(0, 15))

        self.repeatable_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=10, padx=15)
        self.repeatable_entry.grid(row=2, column=3, columnspan=3, sticky='we', pady=10, padx=(0, 15))

        self.generate_btn.grid(row=3, column=0, columnspan=3, sticky='we', padx=(15, 2), pady=20)
        self.ukrainian_lang_btn.grid(row=3, column=3, sticky='we', padx=(2, 2))
        self.change_bg_btn.grid(row=3, column=4, sticky='we', padx=(2, 2))
        self.english_lang_btn.grid(row=3, column=5, sticky='we', padx=(2, 15))

        radiobutton_frame.grid(row=4, column=0, columnspan=6, padx=15, sticky='we')

        self.all_symbols_radio_btn.grid(row=0, column=2, sticky='we', pady=(5, 0))
        self.only_letters_radio_btn.grid(row=0, column=7, sticky='we', pady=(5, 0))
        self.only_digits_radio_btn.grid(row=0, column=12, sticky='we', pady=(5, 0))
        self.letters_digits_radio_btn.grid(row=0, column=17, sticky='we', pady=(5, 0))
        self.letters_signs_radio_btn.grid(row=0, column=22, sticky='we', pady=(5, 0))
        self.digits_signs_radio_btn.grid(row=0, column=27, sticky='we', pady=(5, 0))

        self.all_symbols_label.grid(row=1, column=0, columnspan=5, sticky='we')
        self.only_letters_label.grid(row=1, column=5, columnspan=5, sticky='we')
        self.only_digits_label.grid(row=1, column=10, columnspan=5, sticky='we')
        self.letters_digits_label.grid(row=1, column=15, columnspan=5, sticky='we')
        self.letters_signs_label.grid(row=1, column=20, columnspan=5, sticky='we')
        self.digits_signs_label.grid(row=1, column=25, columnspan=5, sticky='we')

        self.result_password_label.grid(row=5, column=0, pady=(20, 0), columnspan=6)
        self.result_password_entry.grid(row=6, column=0, sticky='nsew', pady=10, padx=15, columnspan=6)

        self.copy_btn.grid(row=7, column=0, columnspan=2, sticky='we', pady=20, padx=(15, 2))
        self.clear_btn.grid(row=7, column=2, columnspan=2, sticky='we', pady=20, padx=(2, 2))
        self.write_to_db_btn.grid(row=7, column=4, columnspan=2, sticky='we', pady=20, padx=(2, 15))

        self.quit_btn.grid(row=8, column=0, columnspan=3, sticky='we', padx=(15, 2), pady=(0, 60))
        self.move_to_table_btn.grid(row=8, column=3, columnspan=3, sticky='we', padx=(2, 15), pady=(0, 60))

        def set_equal_column_width(frame, column_number):
            for column in range(column_number):
                frame.columnconfigure(column, weight=1, uniform="equal")

        CENTER_RADIO_BUTTONS_NUMBER = 30
        set_equal_column_width(radiobutton_frame, CENTER_RADIO_BUTTONS_NUMBER)

        MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE = 6
        set_equal_column_width(main_frame, MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE)

        main_frame.pack(side=TOP, pady=20, padx=20)


class TablePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        full_frame = CTkFrame(self)

        table_frame = CTkFrame(full_frame)
        data_table_obj = TableInterface(table_frame, self.shortcut_search)
        data_table_obj.get_data_from_db(self.current_language_state_bool)

        upper_frame = CTkFrame(full_frame)
        self.synchronize_data_btn = CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['synchronize_data_btn'],
            text_color='black',
            command=lambda: sync_db_data(self.current_language_state_bool, app),
        )

        self.change_token_btn = CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['change_token_btn'],
            text_color='black',
            command=lambda: change_local_token(self.current_language_state_bool, app),
        )

        bottom_frame = CTkFrame(full_frame)
        self.return_to_main_btn = CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['return_to_main_btn'],
            text_color='black',
            command=lambda: controller.show_frame(MainPage)
        )

        self.reload_table_btn = CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['reload_table_btn'],
            text_color='black',
            command=lambda: data_table_obj.get_data_from_db(self.current_language_state_bool),
        )

        self.update_table_btn = CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['update_table_btn'],
            text_color='black',
            command=lambda: update_columns_via_app_interface(self.current_language_state_bool, data_table_obj),
        )

        def delete_record_and_refresh_table():
            remove_status = remove_record_from_table(self.current_language_state_bool, app)
            return None if remove_status is None else data_table_obj.get_data_from_db(self.current_language_state_bool)

        self.delete_record_btn = CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['delete_record_btn'],
            text_color='black',
            command=lambda: delete_record_and_refresh_table(),
        )

        def set_new_language(language: str):
            controller.change_language(language)
            data_table_obj.get_data_from_db(self.current_language_state_bool)

        self.ukrainian_lang_btn = CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['ukrainian_lang_btn'],
            text_color='black',
            command=lambda: set_new_language('UA'),
        )

        self.english_lang_btn = CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['english_lang_btn'],
            text_color='black',
            command=lambda: set_new_language('EN'),
        )

        self.quit_btn = CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['quit_btn'],
            text_color='black',
            command=lambda: app.destroy(),
        )

        self.ukrainian_lang_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.synchronize_data_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.change_token_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.english_lang_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
        upper_frame.pack(fill='both', expand=True)

        table_frame.pack(fill='both', expand=True, pady=5)

        self.return_to_main_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.reload_table_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.update_table_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.delete_record_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.quit_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
        bottom_frame.pack(fill='both', expand=True)

        full_frame.pack(side='top', pady=15)

    def shortcut_search(self, event):
        current_lang = self.controller.current_language
        database_search(event, current_lang)


app = PasswordGeneratorApp()
