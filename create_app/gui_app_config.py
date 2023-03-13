from typing import Optional
from tkinter.constants import TOP

import customtkinter as ctk

from app_translation.load_data_for_localization import localization_data
from create_app.create_sql_table import TableInterface
from create_app.inputs_and_buttons_processing import (
    get_password,
    copy_password,
    write_to_database,
    clear_entries,
    remove_record_from_table,
    database_search,
    update_columns_via_app_interface,
    change_background_color,
    set_equal_column_width,
    # sync_db_data,
    # change_local_token,
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

        main_page.grid(row=0, column=0, sticky='nsew')
        simple_page.grid(row=0, column=0, sticky='nsew')
        table_page.grid(row=0, column=0, sticky='nsew')

        self.frames['main_page'] = main_page
        self.frames['simple_page'] = simple_page
        self.frames['table_page'] = table_page

        self.show_frame('main_page')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_language(self, language: str) -> None:
        for frame in self.frames.values():
            frame.change_language(language)


class BasePage(ctk.CTkFrame):
    DEFAULT_COLOR_THEME: str = 'green'
    DEFAULT_TEXT_COLOR: str = 'black'

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.current_language = 'EN'
        self.current_gen_mode = 'hard'
        ctk.set_default_color_theme(self.DEFAULT_COLOR_THEME)  # set default app theme
        # change_messagebox_color()  # set default bg and font color to messageboxes

    def check_if_app_has_element_type(self, element_type, new_data_text):
        if hasattr(self, element_type):
            button = getattr(self, element_type)
            button.configure(text=new_data_text)

    def parse_localization_json_data(self, options):
        for element_group, group_options in options.items():
            for specific_element, text in group_options.items():
                self.check_if_app_has_element_type(specific_element, text)

    def change_language(self, language: str) -> None:
        if language not in localization_data and language != self.current_language:
            return None
        self.current_language = language
        self.parse_localization_json_data(localization_data.get(language, {}))

    def get_element_name(self, element_type: str, element_name: str) -> Optional[str]:
        return localization_data[self.current_language].get(element_type, {}).get(element_name)

    def create_button(self, frame: ctk.CTkFrame, button_name: str) -> ctk.CTkButton:
        return ctk.CTkButton(
            frame, text=self.get_element_name('buttons', button_name), text_color=self.DEFAULT_TEXT_COLOR
        )

    def create_drop_down_menu(self, frame: ctk.CTkFrame) -> ctk.CTkOptionMenu:
        language_options = [language_option for language_option in localization_data]
        variable = ctk.StringVar(value=language_options[0])
        return ctk.CTkOptionMenu(
            frame,
            values=language_options,
            variable=variable,
            text_color=self.DEFAULT_TEXT_COLOR,
            command=lambda language: self.controller.change_language(language)
        )


class MainPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)

        self.main_frame = ctk.CTkFrame(self)

        self.password_usage_label = self.create_common_label('password_description_label')
        self.password_length_label = self.create_common_label('password_length_label')
        self.repeatable_label = self.create_common_label('repeatable_label')
        self.result_password_label = self.create_common_label('result_password_label')

        self.password_usage_entry = ctk.CTkEntry(self.main_frame)
        self.password_length_entry = ctk.CTkEntry(self.main_frame)
        self.repeatable_entry = ctk.CTkEntry(self.main_frame)
        self.result_password_entry = ctk.CTkEntry(self.main_frame)

        self.radiobutton_choice_option = ctk.IntVar()
        self.radiobutton_choice_option.set(1)  # default option is all symbols

        self.radiobutton_frame = ctk.CTkFrame(self.main_frame)
        self.all_symbols_radio_btn = self.create_radio_button(1)
        self.only_letters_radio_btn = self.create_radio_button(2)
        self.only_digits_radio_btn = self.create_radio_button(3)
        self.letters_digits_radio_btn = self.create_radio_button(4)
        self.letters_signs_radio_btn = self.create_radio_button(5)
        self.digits_signs_radio_btn = self.create_radio_button(6)

        self.all_symbols_label = self.create_radio_button_label('all_symbols_label')
        self.only_letters_label = self.create_radio_button_label('only_letters_label')
        self.only_digits_label = self.create_radio_button_label('only_digits_label')
        self.letters_digits_label = self.create_radio_button_label('letters_digits_label')
        self.letters_signs_label = self.create_radio_button_label('letters_signs_label')
        self.digits_signs_label = self.create_radio_button_label('digits_signs_label')

        self.generate_btn = self.create_button(self.main_frame, 'generate_btn')
        self.generate_btn.configure(command=lambda: get_password(
            self.current_language,
            self.password_usage_entry.get(),
            self.password_length_entry.get(),
            self.repeatable_entry.get(),
            self.radiobutton_choice_option.get(),
            self.result_password_entry,
        ))

        self.copy_btn = self.create_button(self.main_frame, 'copy_btn')
        self.copy_btn.configure(command=lambda: copy_password(
            self.current_language,
            self.result_password_entry.get()
        ))

        self.clear_btn = self.create_button(self.main_frame, 'clear_btn')
        self.clear_btn.configure(command=lambda: clear_entries(
            self.password_usage_entry,
            self.password_length_entry,
            self.repeatable_entry,
            self.result_password_entry
        ))

        self.write_to_db_btn = self.create_button(self.main_frame, 'write_to_db_btn')
        self.write_to_db_btn.configure(command=lambda: write_to_database(
            self.current_language,
            self.password_usage_entry.get(),
            self.result_password_entry.get()
        ))

        self.change_bg_btn = self.create_change_bg_btn()
        self.change_bg_btn.configure(command=lambda: change_background_color(self.change_bg_btn))

        self.move_to_table_btn = self.create_button(self.main_frame, 'move_to_table_btn')
        self.move_to_table_btn.configure(command=lambda: controller.show_frame('table_page'))

        self.quit_btn = self.create_button(self.main_frame, 'quit_btn')
        self.quit_btn.configure(command=lambda: app.destroy())

        self.drop_down_menu = self.create_drop_down_menu(self.main_frame)

        self.place_drop_down_menu()
        self.place_common_labels()
        self.place_radio_buttons()
        self.place_radio_buttons_labels()
        self.place_buttons()

        set_equal_column_width(self.radiobutton_frame, 30)
        set_equal_column_width(self.main_frame, 6)

        self.main_frame.pack(side=TOP, pady=20, padx=20)

    def create_common_label(self, label_name: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(self.main_frame, text=self.get_element_name('labels', label_name))

    def create_radio_button_label(self, label_name: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(self.radiobutton_frame, text=self.get_element_name('radio_buttons_labels', label_name))

    def create_radio_button(self, value: int) -> ctk.CTkRadioButton:
        return ctk.CTkRadioButton(self.radiobutton_frame, text='', variable=self.radiobutton_choice_option, value=value)

    def create_change_bg_btn(self) -> ctk.CTkButton:
        return ctk.CTkButton(self.main_frame, text=u'\u263E', text_color=self.DEFAULT_TEXT_COLOR)

    def place_common_labels(self) -> None:
        self.password_usage_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(30, 10), padx=15)
        self.password_usage_entry.grid(row=0, column=3, columnspan=3, sticky='we', pady=(30, 10), padx=(0, 15))
        self.password_length_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=10, padx=15)
        self.password_length_entry.grid(row=1, column=3, columnspan=3, sticky='we', pady=10, padx=(0, 15))
        self.repeatable_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=10, padx=15)
        self.repeatable_entry.grid(row=2, column=3, columnspan=3, sticky='we', pady=10, padx=(0, 15))
        self.result_password_label.grid(row=5, column=0, pady=(20, 0), columnspan=6)
        self.result_password_entry.grid(row=6, column=0, sticky='nsew', pady=10, padx=15, columnspan=6)

    def place_radio_buttons(self) -> None:
        self.radiobutton_frame.grid(row=4, column=0, columnspan=6, padx=15, sticky='we')
        self.all_symbols_radio_btn.grid(row=0, column=2, sticky='we', pady=(5, 0))
        self.only_letters_radio_btn.grid(row=0, column=7, sticky='we', pady=(5, 0))
        self.only_digits_radio_btn.grid(row=0, column=12, sticky='we', pady=(5, 0))
        self.letters_digits_radio_btn.grid(row=0, column=17, sticky='we', pady=(5, 0))
        self.letters_signs_radio_btn.grid(row=0, column=22, sticky='we', pady=(5, 0))
        self.digits_signs_radio_btn.grid(row=0, column=27, sticky='we', pady=(5, 0))

    def place_radio_buttons_labels(self) -> None:
        self.all_symbols_label.grid(row=1, column=0, columnspan=5, sticky='we')
        self.only_letters_label.grid(row=1, column=5, columnspan=5, sticky='we')
        self.only_digits_label.grid(row=1, column=10, columnspan=5, sticky='we')
        self.letters_digits_label.grid(row=1, column=15, columnspan=5, sticky='we')
        self.letters_signs_label.grid(row=1, column=20, columnspan=5, sticky='we')
        self.digits_signs_label.grid(row=1, column=25, columnspan=5, sticky='we')

    def place_buttons(self) -> None:
        self.generate_btn.grid(row=3, column=0, columnspan=3, sticky='we', padx=(15, 2), pady=20)
        self.change_bg_btn.grid(row=3, column=3, columnspan=2, sticky='we', padx=(2, 2))
        self.copy_btn.grid(row=7, column=0, columnspan=2, sticky='we', pady=20, padx=(15, 2))
        self.clear_btn.grid(row=7, column=2, columnspan=2, sticky='we', pady=20, padx=(2, 2))
        self.write_to_db_btn.grid(row=7, column=4, columnspan=2, sticky='we', pady=20, padx=(2, 15))
        self.quit_btn.grid(row=8, column=0, columnspan=3, sticky='we', padx=(15, 2), pady=(0, 60))
        self.move_to_table_btn.grid(row=8, column=3, columnspan=3, sticky='we', padx=(2, 15), pady=(0, 60))

    def place_drop_down_menu(self) -> None:
        self.drop_down_menu.grid(row=3, column=5, sticky='we', padx=(2, 15))


class SimplePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side=TOP, pady=20, padx=20)


class TablePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        full_frame = ctk.CTkFrame(self, fg_color='transparent')

        self.table_frame = ctk.CTkFrame(full_frame)
        self.data_table_obj = TableInterface(self.table_frame, self.current_language, 800, 430, 20)
        self.data_table_obj.get_data_from_db(self.current_language)

        self.upper_frame = ctk.CTkFrame(full_frame, fg_color='transparent')

        self.synchronize_data_btn = self.create_button(self.upper_frame, 'synchronize_data_btn')
        # self.synchronize_data_btn.configure(command=lambda: sync_db_data(self.current_language, app))

        self.change_token_btn = self.create_button(self.upper_frame, 'change_token_btn')
        # self.change_token_btn.configure(command=lambda: change_local_token(self.current_language, app))

        self.bottom_frame = ctk.CTkFrame(full_frame, fg_color='transparent')

        self.return_to_main_btn = self.create_button(self.bottom_frame, 'return_to_main_btn')
        self.return_to_main_btn.configure(command=lambda: controller.show_frame('main_page'))

        self.reload_table_btn = self.create_button(self.bottom_frame, 'reload_table_btn')
        self.reload_table_btn.configure(command=lambda: self.data_table_obj.reload_table(
            self.table_frame,
            self.current_language
        ))

        self.update_table_btn = self.create_button(self.bottom_frame, 'update_table_btn')
        self.update_table_btn.configure(command=lambda: update_columns_via_app_interface(
            self.current_language,
            self.data_table_obj
        ))

        self.delete_record_btn = self.create_button(self.bottom_frame, 'delete_record_btn')
        self.delete_record_btn.configure(command=lambda: self.delete_record_and_refresh_table())

        self.drop_down_menu = self.create_drop_down_menu(self.upper_frame)

        self.quit_btn = self.create_button(self.bottom_frame, 'quit_btn')
        self.quit_btn.configure(command=lambda: app.destroy())

        self.drop_down_menu.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.synchronize_data_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.change_token_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.upper_frame.pack(fill='both', expand=True)

        self.table_frame.pack(fill='both', expand=True, pady=10)

        self.return_to_main_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
        self.reload_table_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.update_table_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.delete_record_btn.pack(side='left', fill='both', expand=True, padx=(2, 2))
        self.quit_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
        self.bottom_frame.pack(fill='both', expand=True)

        full_frame.pack(side='top', pady=15, padx=15)

    def delete_record_and_refresh_table(self) -> None:
        remove_status = remove_record_from_table(self.current_language, app)
        if remove_status is None:
            return None
        self.data_table_obj.reload_table(self.table_frame, self.current_language)


app = PasswordGeneratorApp()
