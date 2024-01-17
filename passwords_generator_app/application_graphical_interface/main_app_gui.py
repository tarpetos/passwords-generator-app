import customtkinter as ctk

from tkinter import StringVar, PanedWindow
from tkinter.ttk import Separator
from typing import Any

from .modificated_tooltip import ToolTip
from .toplevel_windows_gui import database_search
from .change_background_color import (
    change_appearance_mode,
    change_treeview_frame_elements_color,
)
from .create_sql_table import MainTable

from ..app_translation.load_data_for_localization import LOCALIZATION_DATA
from ..user_actions_processing.inputs_and_buttons_processing import (
    generate_password,
    copy_password,
    write_to_database,
    clear_entries,
    remove_record_from_table,
    simple_generate_password,
    change_encryption_token,
    change_generation_alphabet,
)
from ..user_actions_processing.password_alphabet import PasswordAlphabet


class PasswordGeneratorApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        main_page = MainPage(container, self)
        simple_page = SimplePage(container, self)
        table_page = TablePage(container, self)

        self.frames[MainPage] = main_page
        self.frames[SimplePage] = simple_page
        self.frames[TablePage] = table_page

        self.current_language = "EN"

        self.show_frame(SimplePage)

    current_mode = "simple"

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def change_language(self, language):
        for frame in self.frames.values():
            if isinstance(frame, BasePage):
                self.current_language = frame.change_language(language)

    def destroy_app(self):
        self.destroy()


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.previous_chosen_language = None
        self.current_chosen_language = "EN"
        self.language_options_dict = {
            "EN": "English",
            "UA": "Українська",
            "PL": "Poĺska",
        }
        self.language_options_list = [
            self.language_options_dict[key] for key in self.language_options_dict
        ]
        self.language_opt_menu_var = StringVar(value=self.language_options_list[0])
        self.language_options = LOCALIZATION_DATA  # get data for app localization
        self.alphabet_retriever = PasswordAlphabet()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        change_treeview_frame_elements_color()  # set default bg and font color to messageboxes

    @staticmethod
    def get_lst_index(element: str, lst: list) -> int | None:
        return lst.index(element) if element in lst else None

    @staticmethod
    def set_equal_grid_segments_size(
        frame: ctk.CTkFrame | ctk.CTkToplevel, column_number: int, row_number: int
    ):
        for column in range(column_number):
            frame.columnconfigure(column, weight=1, uniform="equal")

        for row in range(row_number):
            frame.rowconfigure(row, weight=1, uniform="equal")

    def default_value_index(
        self, language: str, element_type: str, current_string_var_value: str
    ) -> int:
        return self.get_lst_index(
            current_string_var_value, self.language_options[language][element_type]
        )

    def configure_elements_with_values_list(
        self, element: Any, element_type: str, new_data: list
    ):
        current_string_var_value = element.cget("variable").get()
        default_value = new_data[
            self.default_value_index(
                self.previous_chosen_language, element_type, current_string_var_value
            )
        ]
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

    def change_language(self, language: str):
        if (
            language in self.language_options
            and self.current_chosen_language != language
        ):
            self.previous_chosen_language = self.current_chosen_language
            self.current_chosen_language = language
            options = self.language_options[language]
            self.parse_localization_json_data(options)
            self.language_opt_menu_var.set(self.language_options_dict[language])

        return self.current_chosen_language


class MainPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)

        alphabet_window = PanedWindow(self)
        alphabet_window.pack(fill="both", expand=True)

        alphabet_frame = ctk.CTkFrame(alphabet_window)
        alphabet_window.add(alphabet_frame)

        letters_label = ctk.CTkLabel(
            alphabet_frame,
            text=LOCALIZATION_DATA["EN"]["toplevel_windows"]["alphabet_window_data"][
                "labels"
            ]["letters_label"],
        )
        letters_entry = ctk.CTkTextbox(alphabet_frame)

        digits_label = ctk.CTkLabel(
            alphabet_frame,
            text=LOCALIZATION_DATA["EN"]["toplevel_windows"]["alphabet_window_data"][
                "labels"
            ]["digits_label"],
        )
        digits_entry = ctk.CTkTextbox(alphabet_frame)

        punctuation_label = ctk.CTkLabel(
            alphabet_frame,
            text=LOCALIZATION_DATA["EN"]["toplevel_windows"]["alphabet_window_data"][
                "labels"
            ]["punctuation_label"],
        )
        punctuation_entry = ctk.CTkTextbox(alphabet_frame)

        save_alphabet_btn = ctk.CTkButton(
            alphabet_frame,
            text=LOCALIZATION_DATA["EN"]["toplevel_windows"]["alphabet_window_data"][
                "buttons"
            ]["save_alphabet_btn"],
            # command=lambda: save_custom_alphabet(
            #     alphabet_store_connector, letters_entry, digits_entry, punctuation_entry
            # )
        )

        reset_alphabet_btn = ctk.CTkButton(
            alphabet_frame,
            text=LOCALIZATION_DATA["EN"]["toplevel_windows"]["alphabet_window_data"][
                "buttons"
            ]["reset_alphabet_btn"],
            # command=lambda: back_to_default_alphabet(
            #     alphabet_store_connector, letters_entry, digits_entry, punctuation_entry
            # )
        )
        #         self.password_description_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=15)
        #         self.password_description_entry.grid(row=0, column=3, columnspan=3, sticky='we', padx=(0, 15))
        #
        #         self.password_length_label.grid(row=1, column=0, columnspan=3, sticky='w', padx=15)
        #         self.slider_frame.grid(row=1, column=3, columnspan=3, sticky='we', padx=(0, 15))
        #         self.password_length_slider.pack(fill='both')
        #         self.password_length_slider_label.pack(fill='both')

        letters_label.grid(row=0, column=0, sticky="w")
        letters_entry.grid(row=0, column=1, sticky="we")

        digits_label.grid(row=1, column=0, sticky="w")
        digits_entry.grid(row=1, column=1, sticky="we")

        punctuation_label.grid(row=2, column=0, sticky="w")
        punctuation_entry.grid(row=2, column=1, sticky="we")

        save_alphabet_btn.grid(row=3, column=0, sticky="we")
        reset_alphabet_btn.grid(row=3, column=1, sticky="we")

        alphabet_frame_column_number = alphabet_frame.grid_size()[0]
        alphabet_frame_row_number = alphabet_frame.grid_size()[1]
        self.set_equal_grid_segments_size(
            alphabet_frame, alphabet_frame_column_number, alphabet_frame_row_number
        )

        generator_window = PanedWindow(alphabet_window, orient="vertical")
        alphabet_window.add(generator_window)

        main_frame = ctk.CTkFrame(generator_window)
        generator_window.add(main_frame)

        self.password_description_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["password_description_label"],
        )
        self.password_length_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["password_length_label"],
        )
        self.repeatable_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["repeatable_label"],
        )
        self.result_password_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["result_password_label"],
        )

        self.password_description_entry = ctk.CTkEntry(main_frame)

        self.slider_frame = ctk.CTkFrame(main_frame)

        def show_current_slider_value(choice):
            self.password_length_slider_label.configure(text=int(choice))

        self.default_pass_length = ctk.IntVar()
        self.default_pass_length.set(50)

        self.password_length_slider = ctk.CTkSlider(
            self.slider_frame,
            from_=1,
            to=500,
            variable=self.default_pass_length,
            command=show_current_slider_value,
        )
        self.password_length_slider.set(50)
        self.password_length_slider_label = ctk.CTkLabel(
            self.slider_frame, text=str(self.default_pass_length.get())
        )

        def check_for_alphabet_length():
            alphabet = self.alphabet_retriever.get_password_alphabet(1)
            if len(alphabet) == 0:
                self.password_length_slider.configure(to=0, state="disabled")
                self.password_length_slider.set(0)
                self.password_length_slider_label.configure(
                    text=self.default_pass_length.get()
                )

        check_for_alphabet_length()

        def slider_value_listener() -> int:
            current_slider_value = self.password_length_slider.get()
            return int(current_slider_value)

        def slider_value_changer():
            initial_slider_value = slider_value_listener()
            not_repeatable_chosen = LOCALIZATION_DATA[self.current_chosen_language][
                "repeatable_segment_btn"
            ][1]
            if self.chosen_button_menu == not_repeatable_chosen:
                new_slider_max_value = len(
                    self.alphabet_retriever.get_password_alphabet(
                        self.radiobutton_choice_option.get()
                    )
                )
                self.password_length_slider.configure(to=new_slider_max_value)
                if new_slider_max_value == 0 or new_slider_max_value == 1:
                    self.password_length_slider.configure(state="disabled")
                else:
                    self.password_length_slider.configure(state="normal")
                if initial_slider_value > new_slider_max_value:
                    self.password_length_slider.set(new_slider_max_value)
                else:
                    self.password_length_slider.set(initial_slider_value)
                show_current_slider_value(slider_value_listener())
            else:
                self.password_length_slider.configure(
                    to=500, variable=self.default_pass_length
                )
                show_current_slider_value(self.default_pass_length.get())

        def selected_button_callback(choice):
            self.chosen_button_menu = choice
            slider_value_changer()

        values_list = list(self.language_options["EN"]["repeatable_segment_btn"])
        self.chosen_button_menu = values_list[0]

        self.default_chosen_btn_var = StringVar(value=self.chosen_button_menu)
        self.repeatable_segment_btn = ctk.CTkSegmentedButton(
            main_frame,
            values=values_list,
            variable=self.default_chosen_btn_var,
            command=selected_button_callback,
        )

        self.result_password_entry = ctk.CTkEntry(main_frame)

        self.radiobutton_choice_option = ctk.IntVar()
        self.radiobutton_choice_option.set(1)  # default option is all symbols

        radiobutton_frame = ctk.CTkFrame(main_frame)

        self.all_symbols_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=1,
            command=slider_value_changer,
        )
        self.all_symbols_radio_btn_tip = ToolTip(
            self.all_symbols_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["all_symbols_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.only_letters_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=2,
            command=slider_value_changer,
        )
        self.only_letters_radio_btn_tip = ToolTip(
            self.only_letters_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["only_letters_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.only_digits_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=3,
            command=slider_value_changer,
        )
        self.only_digits_radio_btn_tip = ToolTip(
            self.only_digits_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["only_digits_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.letters_digits_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=4,
            command=slider_value_changer,
        )
        self.letters_digits_radio_btn_tip = ToolTip(
            self.letters_digits_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["letters_digits_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.letters_signs_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=5,
            command=slider_value_changer,
        )
        self.letters_signs_radio_btn_tip = ToolTip(
            self.letters_signs_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["letters_signs_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.digits_signs_radio_btn = ctk.CTkRadioButton(
            radiobutton_frame,
            text="",
            variable=self.radiobutton_choice_option,
            value=6,
            command=slider_value_changer,
        )
        self.digits_signs_radio_btn_tip = ToolTip(
            self.digits_signs_radio_btn,
            msg=self.language_options["EN"]["tooltips"]["digits_signs_radio_btn_tip"],
            delay=1,
            follow=True,
            label_wrap_length=500,
        )

        self.all_symbols_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "all_symbols_label"
            ],
        )
        self.only_letters_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "only_letters_label"
            ],
        )
        self.only_digits_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "only_digits_label"
            ],
        )
        self.letters_digits_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "letters_digits_label"
            ],
        )
        self.letters_signs_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "letters_signs_label"
            ],
        )
        self.digits_signs_label = ctk.CTkLabel(
            radiobutton_frame,
            text=self.language_options["EN"]["radio_buttons_labels"][
                "digits_signs_label"
            ],
        )

        self.generate_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["generate_btn"],
            command=lambda: generate_password(
                self.current_chosen_language,
                self.password_description_entry,
                self.password_length_slider,
                self.repeatable_segment_btn,
                self.result_password_entry,
                self.alphabet_retriever.get_password_alphabet(
                    self.radiobutton_choice_option.get()
                ),
            ),
        )

        self.copy_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["copy_btn"],
            command=lambda: copy_password(
                self.current_chosen_language, self.result_password_entry
            ),
        )

        self.clear_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["clear_btn"],
            command=lambda: clear_entries(
                self.password_description_entry, self.result_password_entry
            ),
        )

        self.write_to_db_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["write_to_db_btn"],
            command=lambda: write_to_database(
                self.current_chosen_language,
                self.password_description_entry.get(),
                self.result_password_entry.get(),
            ),
        )

        self.new_alphabet_btn = ctk.CTkButton(
            main_frame,
            text=LOCALIZATION_DATA["EN"]["buttons"]["new_alphabet_btn"],
            command=lambda: change_generation_alphabet(self.current_chosen_language),
        )

        def option_language_menu_callback(choice):
            self.chosen_lang_opt_menu = choice
            for key in self.language_options_dict:
                if self.language_options_dict[key] == self.chosen_lang_opt_menu:
                    controller.change_language(key)

        self.language_change_menu = ctk.CTkOptionMenu(
            main_frame,
            values=self.language_options_list,
            variable=self.language_opt_menu_var,
            command=option_language_menu_callback,
        )

        self.change_bg_btn = ctk.CTkButton(
            main_frame,
            text="\u263E",
            command=lambda: change_appearance_mode(self.change_bg_btn),
        )

        def save_page_state():
            controller.current_mode = "simple"
            controller.geometry("900x600")
            controller.show_frame(SimplePage)

        self.simple_mode_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["simple_mode_btn"],
            command=save_page_state,
        )

        def show_table():
            controller.show_frame(TablePage)
            controller.geometry("900x600")

        self.move_to_table_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["move_to_table_btn"],
            command=lambda: show_table(),
        )

        self.quit_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["quit_btn"],
            command=lambda: controller.destroy_app(),
        )

        self.password_description_label.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=15
        )
        self.password_description_entry.grid(
            row=0, column=3, columnspan=3, sticky="we", padx=(0, 15)
        )

        self.password_length_label.grid(
            row=1, column=0, columnspan=3, sticky="w", padx=15
        )
        self.slider_frame.grid(row=1, column=3, columnspan=3, sticky="we", padx=(0, 15))
        self.password_length_slider.pack(fill="both")
        self.password_length_slider_label.pack(fill="both")

        self.repeatable_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=15)
        self.repeatable_segment_btn.grid(
            row=2, column=3, columnspan=3, sticky="we", padx=(0, 15)
        )

        self.generate_btn.grid(row=3, column=0, columnspan=3, sticky="we", padx=(15, 2))

        self.new_alphabet_btn.grid(row=3, column=3, sticky="we", padx=(2, 2))
        self.language_change_menu.grid(row=3, column=4, sticky="we", padx=(2, 2))
        self.change_bg_btn.grid(row=3, column=5, sticky="we", padx=(2, 15))

        radiobutton_frame.grid(row=4, column=0, columnspan=6, padx=15, sticky="we")

        self.all_symbols_radio_btn.grid(row=0, column=2, sticky="we", pady=(5, 0))
        self.only_letters_radio_btn.grid(row=0, column=7, sticky="we", pady=(5, 0))
        self.only_digits_radio_btn.grid(row=0, column=12, sticky="we", pady=(5, 0))
        self.letters_digits_radio_btn.grid(row=0, column=17, sticky="we", pady=(5, 0))
        self.letters_signs_radio_btn.grid(row=0, column=22, sticky="we", pady=(5, 0))
        self.digits_signs_radio_btn.grid(row=0, column=27, sticky="we", pady=(5, 0))

        self.all_symbols_label.grid(row=1, column=0, columnspan=5, sticky="we")
        self.only_letters_label.grid(row=1, column=5, columnspan=5, sticky="we")
        self.only_digits_label.grid(row=1, column=10, columnspan=5, sticky="we")
        self.letters_digits_label.grid(row=1, column=15, columnspan=5, sticky="we")
        self.letters_signs_label.grid(row=1, column=20, columnspan=5, sticky="we")
        self.digits_signs_label.grid(row=1, column=25, columnspan=5, sticky="we")

        self.result_password_label.grid(row=5, column=0, columnspan=6)
        self.result_password_entry.grid(
            row=6, column=0, sticky="nsew", padx=15, columnspan=6
        )

        self.copy_btn.grid(row=7, column=0, columnspan=2, sticky="we", padx=(15, 2))
        self.clear_btn.grid(row=7, column=2, columnspan=2, sticky="we", padx=(2, 2))
        self.write_to_db_btn.grid(
            row=7, column=4, columnspan=2, sticky="we", padx=(2, 15)
        )

        self.quit_btn.grid(
            row=8, column=0, columnspan=2, sticky="we", padx=(15, 2), pady=(0, 15)
        )
        self.simple_mode_btn.grid(
            row=8, column=2, columnspan=2, sticky="we", padx=(2, 2), pady=(0, 15)
        )
        self.move_to_table_btn.grid(
            row=8, column=4, columnspan=2, sticky="we", padx=(2, 15), pady=(0, 15)
        )

        radiobutton_frame_column_number = radiobutton_frame.grid_size()[0]
        radiobutton_frame_row_number = radiobutton_frame.grid_size()[1]

        main_frame_column_number = main_frame.grid_size()[0]
        main_frame_row_number = main_frame.grid_size()[1]

        self.set_equal_grid_segments_size(
            radiobutton_frame,
            radiobutton_frame_column_number,
            radiobutton_frame_row_number,
        )
        self.set_equal_grid_segments_size(
            main_frame, main_frame_column_number, main_frame_row_number
        )


class SimplePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)

        main_frame = ctk.CTkFrame(self)

        self.password_description_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["password_description_label"],
        )
        self.result_password_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["result_password_label"],
        )
        self.option_menu_label = ctk.CTkLabel(
            main_frame,
            text=self.language_options["EN"]["labels"]["option_menu_label"],
        )

        self.password_description_entry = ctk.CTkEntry(main_frame)
        self.result_password_entry = ctk.CTkEntry(main_frame)

        def option_menu_callback(choice):
            self.chosen_opt_menu = choice

        values_list = list(self.language_options["EN"]["symbols_option_menu"])
        self.chosen_opt_menu = values_list[4]

        self.default_opt_menu_var = StringVar(value=self.chosen_opt_menu)
        self.symbols_option_menu = ctk.CTkOptionMenu(
            main_frame,
            values=values_list,
            variable=self.default_opt_menu_var,
            command=option_menu_callback,
        )

        def switch_callback():
            self.switch_state = not self.switch_state

        self.switch_state = False
        self.write_to_db_switch = ctk.CTkSwitch(
            main_frame,
            text=self.language_options["EN"]["switches"]["write_to_db_switch"],
            command=switch_callback,
        )

        self.write_to_db_switch_tip = ToolTip(
            self.write_to_db_switch,
            msg=self.language_options["EN"]["tooltips"]["write_to_db_switch_tip"],
            delay=0.5,
            follow=True,
        )

        self.upper_separator = Separator(main_frame, orient="horizontal")
        self.bottom_separator = Separator(main_frame, orient="horizontal")

        self.generate_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["generate_btn"],
            command=lambda: simple_generate_password(
                self.current_chosen_language,
                self.result_password_entry,
                self.symbols_option_menu,
                self.password_description_entry,
                self.switch_state,
                self.alphabet_retriever.get_full_alphabet(),
            ),
        )

        def save_page_state():
            controller.current_mode = "hard"
            controller.geometry("1100x600")
            controller.show_frame(MainPage)

        self.hard_mode_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["hard_mode_btn"],
            command=save_page_state,
        )

        self.move_to_table_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["move_to_table_btn"],
            command=lambda: controller.show_frame(TablePage),
        )

        self.quit_btn = ctk.CTkButton(
            main_frame,
            text=self.language_options["EN"]["buttons"]["quit_btn"],
            command=lambda: controller.destroy_app(),
        )

        self.password_description_label.grid(row=0, column=0, sticky="w", padx=15)
        self.password_description_entry.grid(
            row=0, column=1, columnspan=2, sticky="we", padx=15
        )

        self.option_menu_label.grid(row=1, column=0, sticky="w", padx=15)
        self.symbols_option_menu.grid(row=1, column=1, sticky="we", padx=15)
        self.write_to_db_switch.grid(row=1, column=2, sticky="e", padx=(0, 15))

        self.upper_separator.grid(
            row=2, column=0, columnspan=3, sticky="we", pady=(0, 5), padx=15
        )

        self.result_password_label.grid(row=3, column=0, pady=(20, 0), columnspan=3)
        self.result_password_entry.grid(
            row=4, column=0, sticky="nsew", pady=10, padx=15, columnspan=3
        )

        self.generate_btn.grid(
            row=5, column=0, columnspan=3, sticky="we", pady=(5, 0), padx=15
        )

        self.bottom_separator.grid(row=6, column=0, columnspan=3, sticky="we", padx=15)

        self.quit_btn.grid(row=7, column=0, sticky="we", padx=(15, 2), pady=(0, 15))
        self.hard_mode_btn.grid(row=7, column=1, sticky="we", padx=(2, 2), pady=(0, 15))
        self.move_to_table_btn.grid(
            row=7, column=2, sticky="we", padx=(2, 15), pady=(0, 15)
        )

        main_frame_column_number = main_frame.grid_size()[0]
        main_frame_row_number = main_frame.grid_size()[1]
        self.set_equal_grid_segments_size(
            main_frame, main_frame_column_number, main_frame_row_number
        )

        main_frame.pack(side="top", pady=20, padx=20, expand=True, fill="both")


class TablePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        full_frame = ctk.CTkFrame(self, fg_color="transparent")

        table_frame = ctk.CTkFrame(full_frame)
        data_table_obj = MainTable(
            table_frame,
            self.current_chosen_language,
            self.shortcut_search,
            200,
            200,
            20,
        )
        data_table_obj.get_data_from_db(self.current_chosen_language)

        upper_frame = ctk.CTkFrame(full_frame, fg_color="transparent")

        self.change_encryption_token_btn = ctk.CTkButton(
            upper_frame,
            text=self.language_options["EN"]["buttons"]["change_encryption_token_btn"],
            command=lambda: change_encryption_token(self.current_chosen_language),
        )

        bottom_frame = ctk.CTkFrame(full_frame, fg_color="transparent")

        def back_to_parent_page():
            if controller.current_mode == "hard":
                controller.show_frame(MainPage)
                controller.geometry("1100x600")
            else:
                controller.show_frame(SimplePage)
                controller.geometry("900x600")

        self.return_to_main_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options["EN"]["buttons"]["return_to_main_btn"],
            command=back_to_parent_page,
        )

        self.reload_table_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options["EN"]["buttons"]["reload_table_btn"],
            command=lambda: data_table_obj.reload_table(
                table_frame, self.shortcut_search, self.current_chosen_language
            ),
        )

        def delete_record_and_refresh_table():
            remove_status = remove_record_from_table(self.current_chosen_language)
            return (
                None
                if remove_status is None
                else data_table_obj.reload_table(
                    table_frame, self.shortcut_search, self.current_chosen_language
                )
            )

        self.delete_record_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options["EN"]["buttons"]["delete_record_btn"],
            command=lambda: delete_record_and_refresh_table(),
        )

        def table_pg_option_language_menu_callback(choice):
            self.table_pg_chosen_lang_opt_menu = choice
            for key in self.language_options_dict:
                if (
                    self.language_options_dict[key]
                    == self.table_pg_chosen_lang_opt_menu
                ):
                    controller.change_language(key)

        self.table_pg_language_change_menu = ctk.CTkOptionMenu(
            upper_frame,
            values=self.language_options_list,
            variable=self.language_opt_menu_var,
            command=table_pg_option_language_menu_callback,
        )

        self.quit_btn = ctk.CTkButton(
            bottom_frame,
            text=self.language_options["EN"]["buttons"]["quit_btn"],
            command=lambda: controller.destroy_app(),
        )

        self.table_pg_language_change_menu.pack(
            side="left", fill="both", expand=True, padx=(0, 2)
        )
        self.change_encryption_token_btn.pack(
            side="right", fill="both", expand=True, padx=(2, 0)
        )
        upper_frame.pack(fill="both")

        table_frame.pack(fill="both", expand=True, pady=10)

        self.return_to_main_btn.pack(side="left", fill="both", expand=True, padx=(0, 2))
        self.reload_table_btn.pack(side="left", fill="both", expand=True, padx=(2, 2))
        self.delete_record_btn.pack(side="left", fill="both", expand=True, padx=(2, 2))
        self.quit_btn.pack(side="left", fill="both", expand=True, padx=(2, 0))
        bottom_frame.pack(fill="both")

        full_frame.pack(side="top", pady=20, padx=20, expand=True, fill="both")

    def shortcut_search(self, event):
        current_lang = self.controller.current_language
        database_search(event, current_lang)
