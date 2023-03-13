import customtkinter as ctk

from tkinter import StringVar
from tkinter.constants import TOP
from tkinter.ttk import Separator
from typing import Any

from .toplevel_windows import database_search
from .change_background_color import change_background_color, change_element_bg_color
from .create_sql_table import TableInterface

from ..app_translation.load_data_for_localization import all_json_localization_data
from ..user_actions_processing.inputs_and_buttons_processing import (
    generate_password,
    copy_password,
    write_to_database,
    clear_entries,
    remove_record_from_table,
    sync_db_data,
    change_local_token,
    simple_generate_password,
)


class PasswordGeneratorApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        container = ctk.CTkFrame(self)
        container.pack(side=TOP, fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        main_page = MainPage(container, self)
        simple_page = SimplePage(container, self)
        table_page = TablePage(container, self)

        self.frames[MainPage] = main_page
        self.frames[SimplePage] = simple_page
        self.frames[TablePage] = table_page

        main_page.grid(row=0, column=0, sticky='nsew')
        simple_page.grid(row=0, column=0, sticky='nsew')
        table_page.grid(row=0, column=0, sticky='nsew')

        self.current_language = True

        self.show_frame(SimplePage)

    current_mode = 'simple'

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_language(self, language):
        for frame in self.frames.values():
            if isinstance(frame, BasePage):
                self.current_language = frame.change_language(language)


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.current_language_state_bool = True
        self._current_language_state_str = 'EN'
        self.language_options = all_json_localization_data  # get data for app localization
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')  # set default app theme
        change_element_bg_color()  # set default bg and font color to messageboxes

    @staticmethod
    def make_language_state_boolean(language):
        return True if language == 'EN' else False

    @staticmethod
    def get_lst_index(element: str, lst: list) -> int | None:
        return lst.index(element) if element in lst else None

    def default_value_index(self, language: str, element_type: str, current_string_var_value: str) -> int:
        return self.get_lst_index(current_string_var_value, self.language_options[language][element_type])

    def configure_elements_with_values_list(self, element: Any, element_type: str, new_data: list):
        current_string_var_value = element.cget('variable').get()

        default_value = ''
        if self._current_language_state_str == 'EN':
            default_value = new_data[self.default_value_index('UA', element_type, current_string_var_value)]
        elif self._current_language_state_str == 'UA':
            default_value = new_data[self.default_value_index('EN', element_type, current_string_var_value)]

        default_var = StringVar(value=default_value)
        element.configure(values=new_data, variable=default_var)

    def element_configure(self, element, element_type, new_data):
        if isinstance(element, ctk.CTkSegmentedButton):
            self.configure_elements_with_values_list(element, element_type, new_data)
        elif isinstance(element, ctk.CTkOptionMenu):
            self.configure_elements_with_values_list(element, element_type, new_data)
        else:
            element.configure(text=new_data)

    def check_for_element(self, element_type, new_data):
        if hasattr(self, element_type):
            element = getattr(self, element_type)
            self.element_configure(element, element_type, new_data)

    def choose_between_dict_or_list(self, element_group, group_options):
        if isinstance(group_options, list):
            self.check_for_element(element_group, group_options)
        else:
            for specific_element, text in group_options.items():
                self.check_for_element(specific_element, text)

    def parse_localization_json_data(self, options):
        for element_group, group_options in options.items():
            self.choose_between_dict_or_list(element_group, group_options)

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

        main_frame = ctk.CTkFrame(self)

        self.password_usage_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['password_usage_label']
        )
        self.password_length_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['password_length_label'],
        )
        self.repeatable_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['repeatable_label'],
        )
        self.result_password_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['result_password_label'],
        )

        self.password_usage_entry = ctk.CTkEntry(main_frame)

        self.slider_frame = ctk.CTkFrame(main_frame)

        def print_slider(choice):
            self.password_length_slider_label.configure(text=int(choice))

        default_pass_length = ctk.IntVar()
        default_pass_length.set(50)

        self.password_length_slider = ctk.CTkSlider(
            self.slider_frame,
            from_=1, to=500,
            variable=default_pass_length,
            command=print_slider
        )
        self.password_length_slider_label = ctk.CTkLabel(self.slider_frame, text=str(default_pass_length.get()))

        def selected_button_callback(choice):
            self.chosen_button_menu = choice

        values_list = list(self.language_options['EN']['repeatable_segment_btn'])
        self.chosen_button_menu = values_list[0]

        self.default_chosen_btn_var = StringVar(value=self.chosen_button_menu)
        self.repeatable_segment_btn = ctk.CTkSegmentedButton(
            main_frame,
            values=values_list,
            variable=self.default_chosen_btn_var,
            command=selected_button_callback
        )

        self.result_password_entry = ctk.CTkEntry(main_frame)

        radiobutton_choice_option = ctk.IntVar()
        radiobutton_choice_option.set(1)  # default option is all symbols

        radiobutton_frame = ctk.CTkFrame(main_frame)

        self.all_symbols_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=1,
        )
        self.only_letters_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=2,
        )
        self.only_digits_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=3,
        )
        self.letters_digits_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=4,
        )
        self.letters_signs_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=5,
        )
        self.digits_signs_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text='',
            variable=radiobutton_choice_option,
            value=6,

        )

        self.all_symbols_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['all_symbols_label']
        )
        self.only_letters_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['only_letters_label']
        )
        self.only_digits_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['only_digits_label']
        )
        self.letters_digits_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['letters_digits_label']
        )
        self.letters_signs_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['letters_signs_label']
        )
        self.digits_signs_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options['EN']['radio_buttons_labels']['digits_signs_label']
        )

        self.generate_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['generate_btn'],
            text_color='black',
            command=lambda: generate_password(
                self.current_language_state_bool,
                self.password_usage_entry,
                self.password_length_slider,
                self.repeatable_segment_btn,
                self.result_password_entry,
                radiobutton_choice_option
            ),
        )

        self.copy_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['copy_btn'],
            text_color='black',
            command=lambda: copy_password(self.current_language_state_bool, self.result_password_entry),
        )

        self.clear_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['clear_btn'],
            text_color='black',
            command=lambda: clear_entries(
                self.password_usage_entry,
                self.result_password_entry
            ),
        )

        self.write_to_db_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['write_to_db_btn'],
            text_color='black',
            command=lambda: write_to_database(
                self.current_language_state_bool,
                self.password_usage_entry.get(),
                self.result_password_entry.get()
            ),
        )

        self.change_bg_btn = ctk.CTkButton(
            main_frame,
            text=u'\u263E',
            text_color='black',
            command=lambda: change_background_color(self.change_bg_btn),
        )

        def save_page_state():
            controller.current_mode = 'simple'
            controller.show_frame(SimplePage)

        self.simple_mode_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['simple_mode_btn'],
            text_color='black',
            command=save_page_state,
        )

        self.move_to_table_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['move_to_table_btn'],
            text_color='black',
            command=lambda: controller.show_frame(TablePage),
        )

        self.ukrainian_lang_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['ukrainian_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('UA'),
        )

        self.english_lang_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['english_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('EN')
        )

        self.quit_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['quit_btn'],
            text_color='black',
            command=lambda: app.destroy(),
        )

        self.password_usage_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(30, 10), padx=15)
        self.password_usage_entry.grid(row=0, column=3, columnspan=3, sticky='we', pady=(30, 10), padx=(0, 15))

        self.password_length_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=5, padx=15)
        self.slider_frame.grid(row=1, column=3, columnspan=3, sticky='we', pady=5, padx=(0, 15))
        self.password_length_slider.pack(fill='both')
        self.password_length_slider_label.pack(fill='both')

        self.repeatable_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=10, padx=15)
        self.repeatable_segment_btn.grid(row=2, column=3, columnspan=3, sticky='we', pady=10, padx=(0, 15))

        self.generate_btn.grid(row=3, column=0, columnspan=3, sticky='we', padx=(15, 2), pady=15)
        self.ukrainian_lang_btn.grid(row=3, column=3, sticky='we', padx=(2, 2), pady=15)
        self.change_bg_btn.grid(row=3, column=4, sticky='we', padx=(2, 2), pady=15)
        self.english_lang_btn.grid(row=3, column=5, sticky='we', padx=(2, 15), pady=15)

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

        self.quit_btn.grid(row=8, column=0, columnspan=2, sticky='we', padx=(15, 2), pady=(0, 60))
        self.simple_mode_btn.grid(row=8, column=2, columnspan=2, sticky='we', padx=(2, 2), pady=(0, 60))
        self.move_to_table_btn.grid(row=8, column=4, columnspan=2, sticky='we', padx=(2, 15), pady=(0, 60))

        def set_equal_column_width(frame, column_number):
            for column in range(column_number):
                frame.columnconfigure(column, weight=1, uniform='equal')

        self.CENTER_RADIO_BUTTONS_NUMBER = 30
        self.MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE = 6

        set_equal_column_width(radiobutton_frame, self.CENTER_RADIO_BUTTONS_NUMBER)
        set_equal_column_width(main_frame, self.MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE)

        main_frame.pack(side=TOP, pady=20, padx=20, expand=True, fill='both')


class SimplePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)

        main_frame = ctk.CTkFrame(self)

        self.password_usage_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['password_usage_label']
        )
        self.result_password_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['result_password_label'],
        )
        self.option_menu_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options['EN']['labels']['option_menu_label'],
        )

        self.password_usage_entry = ctk.CTkEntry(main_frame)
        self.result_password_entry = ctk.CTkEntry(main_frame)

        def option_menu_callback(choice):
            self.chosen_opt_menu = choice

        values_list = list(self.language_options['EN']['symbols_option_menu'])
        self.chosen_opt_menu = values_list[4]

        self.default_opt_menu_var = StringVar(value=self.chosen_opt_menu)
        self.symbols_option_menu = ctk.CTkOptionMenu(
            main_frame,
            text_color='black',
            values=values_list,
            variable=self.default_opt_menu_var,
            command=option_menu_callback
        )

        def switch_callback():
            self.switch_state = not self.switch_state

        self.switch_state = False
        self.write_to_db_switch = ctk.CTkSwitch(
            main_frame,
            text=self.language_options['EN']['switches']['write_to_db_switch'],
            command=switch_callback,
        )

        self.upper_separator = Separator(main_frame, orient='horizontal')
        self.bottom_separator = Separator(main_frame, orient='horizontal')

        self.generate_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['generate_btn'],
            text_color='black',
            command=lambda: simple_generate_password(
                self.current_language_state_bool,
                self.result_password_entry,
                self.symbols_option_menu,
                self.password_usage_entry,
                self.switch_state
            ),
        )

        def save_page_state():
            controller.current_mode = 'hard'
            controller.show_frame(MainPage)

        self.hard_mode_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['hard_mode_btn'],
            text_color='black',
            command=save_page_state,
        )

        self.move_to_table_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['move_to_table_btn'],
            text_color='black',
            command=lambda: controller.show_frame(TablePage),
        )

        self.quit_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options['EN']['buttons']['quit_btn'],
            text_color='black',
            command=lambda: app.destroy(),
        )

        self.password_usage_label.grid(row=0, column=0, sticky='w', pady=(30, 0), padx=15)
        self.password_usage_entry.grid(row=0, column=1, columnspan=2, sticky='we', pady=(30, 0), padx=(0, 15))

        self.option_menu_label.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=15)
        self.symbols_option_menu.grid(row=1, column=1, sticky='we', pady=(5, 0), padx=15)
        self.write_to_db_switch.grid(row=1, column=2, sticky='e', pady=(5, 0), padx=(0, 15))

        self.upper_separator.grid(row=2, column=0, columnspan=3, sticky='we', pady=(0, 5), padx=15)

        self.result_password_label.grid(row=3, column=0, pady=(20, 0), columnspan=3)
        self.result_password_entry.grid(row=4, column=0, sticky='nsew', pady=10, padx=15, columnspan=3)

        self.generate_btn.grid(row=5, column=0, columnspan=3, sticky='we', pady=(5, 0), padx=15)

        self.bottom_separator.grid(row=6, column=0, columnspan=3, sticky='we', padx=15)

        self.quit_btn.grid(row=7, column=0, sticky='we', padx=(15, 2), pady=(0, 35))
        self.hard_mode_btn.grid(row=7, column=1, sticky='we', padx=(2, 2), pady=(0, 35))
        self.move_to_table_btn.grid(row=7, column=2, sticky='we', padx=(2, 15), pady=(0, 35))

        def set_equal_column_width(frame, column_number):
            for column in range(column_number):
                frame.columnconfigure(column, weight=1, uniform='equal')

        def set_row_height(frame, row_number):
            for column in range(row_number):
                frame.rowconfigure(column, weight=1, uniform='equal')

        self.MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE = 3
        self.MAIN_WINDOW_EQUAL_GRID_ROW_SIZE = 7

        set_equal_column_width(main_frame, self.MAIN_WINDOW_EQUAL_GRID_COLUMNS_SIZE)
        set_row_height(main_frame, self.MAIN_WINDOW_EQUAL_GRID_ROW_SIZE)

        main_frame.pack(side=TOP, pady=20, padx=20, expand=True, fill='both')


class TablePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        full_frame = ctk.CTkFrame(self, fg_color='transparent')

        table_frame = ctk.CTkFrame(full_frame)
        data_table_obj = TableInterface(
            table_frame, self.current_language_state_bool, self.shortcut_search, 200, 200, 20
        )
        data_table_obj.get_data_from_db(self.current_language_state_bool)

        upper_frame = ctk.CTkFrame(full_frame, fg_color='transparent')
        self.synchronize_data_btn = ctk.CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['synchronize_data_btn'],
            text_color='black',
            command=lambda: sync_db_data(self.current_language_state_bool),
        )

        self.change_token_btn = ctk.CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['change_token_btn'],
            text_color='black',
            command=lambda: change_local_token(self.current_language_state_bool),
        )

        bottom_frame = ctk.CTkFrame(full_frame, fg_color='transparent')

        def back_to_parent_page():
            controller.show_frame(MainPage) if controller.current_mode == 'hard' else controller.show_frame(SimplePage)

        self.return_to_main_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['return_to_main_btn'],
            text_color='black',
            command=back_to_parent_page
        )

        self.reload_table_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['reload_table_btn'],
            text_color='black',
            command=lambda: data_table_obj.reload_table(
                table_frame,
                self.shortcut_search,
                self.current_language_state_bool
            ),
        )

        def delete_record_and_refresh_table():
            remove_status = remove_record_from_table(self.current_language_state_bool)
            return None if remove_status is None else data_table_obj.reload_table(
                table_frame,
                self.shortcut_search,
                self.current_language_state_bool
            )

        self.delete_record_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['delete_record_btn'],
            text_color='black',
            command=lambda: delete_record_and_refresh_table(),
        )

        self.ukrainian_lang_btn = ctk.CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['ukrainian_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('UA'),
        )

        self.english_lang_btn = ctk.CTkButton(
            upper_frame,
            text=self.language_options['EN']['buttons']['english_lang_btn'],
            text_color='black',
            command=lambda: controller.change_language('EN'),
        )

        self.quit_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options['EN']['buttons']['quit_btn'],
            text_color='black',
            command=lambda: app.destroy(),
        )

        self.ukrainian_lang_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.synchronize_data_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.change_token_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.english_lang_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
        upper_frame.pack(fill='both')

        table_frame.pack(fill='both', expand=True, pady=10)

        self.return_to_main_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.reload_table_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.delete_record_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.quit_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
        bottom_frame.pack(fill='both')

        full_frame.pack(side=TOP, pady=20, padx=20, expand=True, fill='both')

    def shortcut_search(self, event):
        current_lang = self.controller.current_language
        database_search(event, current_lang)


app = PasswordGeneratorApp()
