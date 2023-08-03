from customtkinter import (
    CTkLabel,
    CTkFrame,
    CTkEntry,
    CTkToplevel,
    CTkProgressBar,
    CTkButton,
    get_appearance_mode,
)

from tkinter import ttk, StringVar
from typing import Dict, Any, Tuple, List

from .create_sql_table import retrieve_data_for_build_table_interface, SearchTable, HistoryTable
from ..app_translation.load_data_for_localization import json_localization_data

from ..app_translation.messagebox_with_lang_change import (
    search_query_input_message,
    no_matches_for_search_message,
    invalid_search_query_message
)
from ..database_connections.alphabet_store import AlphabetStore

from ..user_actions_processing.password_strength_score import (
    password_strength,
    make_score_proportion,
    strength_rating,
    password_strength_chat_gpt,
)

from ..user_actions_processing.default_alphabet import DEFAULT_LETTERS, \
    DEFAULT_DIGITS, DEFAULT_PUNCTUATION, NOT_ALLOWED_PUNCTUATION

MAX_SEARCH_QUERY_LENGTH = 500


# class ToplevelWindow(CTkToplevel):
#     DEFAULT_TOPLEVEL_WIDTH = 700
#     DEFAULT_TOPLEVEL_HEIGHT = 300
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.wait_visibility()
#         self.grab_set()
#         # self.dark = 'dark'
#         # self.light = 'light'
#         # self.black = 'black'
#         # self.white = 'white'
#         # self.current_appearance_mode = get_appearance_mode()
#
#     @staticmethod
#     def label_builder(
#             root: CTkFrame | CTkCanvas | CTkToplevel | CTk,
#             text: str,
#             text_color: str = None,
#             fg_color: str = None,
#             font: Tuple[str, int] = None
#     ) -> CTkLabel:
#         return CTkLabel(root, text=text, text_color=text_color, fg_color=fg_color, font=font)
#
#     @staticmethod
#     def entry_builder(root: CTkFrame | CTkCanvas | CTkToplevel | CTk) -> CTkEntry:
#         return CTkEntry(root)
#
#     @staticmethod
#     def button_builder(root: CTkFrame | CTkCanvas | CTkToplevel | CTk) -> CTkButton:
#         return CTkButton(root)
#
#     @staticmethod
#     def frame_builder(root: CTkFrame | CTkCanvas | CTkToplevel | CTk) -> CTkFrame:
#         return CTkFrame(root)
#
#     @staticmethod
#     def progress_bar_builder(root: CTkFrame | CTkCanvas | CTkToplevel | CTk) -> CTkProgressBar:
#         return CTkProgressBar(root)
#
#     @staticmethod
#     def canvas_builder(root: CTkFrame | CTkCanvas | CTkToplevel | CTk) -> CTkCanvas:
#         return CTkCanvas(root)
#
#     def set_window_title(self, second_part: str = 'additional window') -> None:
#         self.title(f'Password Generator: {second_part}')
#
#     def set_window_size(self, width: int = DEFAULT_TOPLEVEL_WIDTH, height: int = DEFAULT_TOPLEVEL_HEIGHT) -> None:
#         self.geometry(f'{width}x{height}')
#         self.minsize(width, height)


def generator_history_screen(lang_state: str):
    history_window = CTkToplevel()
    history_window.title('Password Generator: generation history')
    history_window.geometry('900x502')
    history_window.minsize(900, 502)
    history_window.wait_visibility()
    history_window.grab_set()

    history_frame = CTkFrame(history_window)

    info_label = CTkLabel(
        history_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['history_window_data']
    )

    info_label.pack(side='top', expand=True, fill='both', pady=10)

    data_for_table = HistoryTable(history_frame, lang_state, 200, 200, 20)
    data_for_table.get_data_from_db(lang_state)

    history_frame.pack(pady=10, padx=10)

    history_window.mainloop()


def password_strength_screen(lang_state: str):
    strength_window = CTkToplevel()
    strength_window.title('Password Generator: strength checker')
    strength_window.geometry('750x350')
    strength_window.minsize(750, 350)
    strength_window.wait_visibility()
    strength_window.grab_set()

    strength_frame = CTkFrame(strength_window)

    enter_label = CTkLabel(
        strength_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['strength_window_data']['enter_label']
    )

    shanon_score_label = CTkLabel(
        strength_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['strength_window_data']['shanon_score_label']
    )

    ai_score_label = CTkLabel(
        strength_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['strength_window_data']['ai_score_label']
    )

    average_score_label = CTkLabel(
        strength_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['strength_window_data']['average_score_label']
    )

    reliability_label = CTkLabel(
        strength_frame,
        text=json_localization_data[lang_state]['toplevel_windows']['strength_window_data']['reliability_label']
    )

    shanon_score_value_label = CTkLabel(strength_frame, text='—')
    ai_score_value_label = CTkLabel(strength_frame, text='—')
    average_score_value_label = CTkLabel(strength_frame, text='—')
    reliability_value_label = CTkLabel(strength_frame, text='—')

    strength_labels = (
        shanon_score_value_label, ai_score_value_label, average_score_value_label, reliability_value_label
    )

    def entry_modified(str_var: StringVar):
        rating = strength_check(str_var, lang_state, strength_labels)
        update_rectangle(rating)

    str_var_modifier = StringVar()
    str_var_modifier.trace('w', lambda name, index, mode, sv=str_var_modifier: entry_modified(sv))
    password_input_entry = CTkEntry(strength_frame, textvariable=str_var_modifier, width=300)

    def set_progress_default_color():
        current_mode = get_appearance_mode()
        return '#939BA2' if current_mode == 'Light' else '#4A4D50'

    default_progress_bar_color = set_progress_default_color()
    strength_bar = CTkProgressBar(strength_frame, height=20, progress_color=default_progress_bar_color)
    strength_bar.set(0)

    separator = ttk.Separator(strength_frame, orient='horizontal')

    enter_label.grid(column=0, row=0, sticky='w', padx=10)
    password_input_entry.grid(column=1, row=0, sticky='we', padx=(0, 10))
    separator.grid(column=0, row=1, columnspan=2, sticky='we', padx=10)

    shanon_score_label.grid(column=0, row=2, sticky='w', padx=10)
    shanon_score_value_label.grid(column=1, row=2, sticky='w')
    ai_score_label.grid(column=0, row=3, sticky='w', padx=10)
    ai_score_value_label.grid(column=1, row=3, sticky='w')
    average_score_label.grid(column=0, row=4, sticky='w', padx=10)
    average_score_value_label.grid(column=1, row=4, sticky='w')
    reliability_label.grid(column=0, row=5, sticky='w', padx=10)
    reliability_value_label.grid(column=1, row=5, sticky='w')

    strength_bar.grid(column=0, row=6, columnspan=2, sticky='we', padx=50)

    strength_bar.update_idletasks()

    strength_frame_column_number = strength_frame.grid_size()[0]
    strength_frame_row_number = strength_frame.grid_size()[1]
    set_equal_grid_segments_size(strength_frame, strength_frame_column_number, strength_frame_row_number)

    strength_frame.pack(expand=True, fill='both', padx=10, pady=10)

    def update_rectangle(rating: float):
        progress = rating / 100
        strength_bar.set(progress)
        gradient = ['#FF0000', '#FF4D00', '#FF9900', '#FFFF00', '#BFFF00', '#00FF00']
        color_index = int(progress * len(gradient))
        color_index = min(color_index, 5)
        color = gradient[color_index]
        strength_bar.configure(progress_color=default_progress_bar_color if rating == 0 else color)

    def on_close():
        strength_window.destroy()
        strength_window.quit()

    strength_window.wm_protocol('WM_DELETE_WINDOW', on_close)

    strength_window.mainloop()


def loop_trough_scores_tuple(strength_tpl: tuple, tpl=('—', '—', '—', '—')):
    for tuple_index, tuple_value in enumerate(tpl):
        strength_tpl[tuple_index].configure(text=tuple_value)


def strength_check(
        str_var_modifier: StringVar,
        lang_state: str,
        strength_labels: Tuple[CTkLabel, CTkLabel, CTkLabel, CTkLabel]
) -> int:
    user_input = str_var_modifier.get()

    if not user_input:
        loop_trough_scores_tuple(strength_labels)
        return 0

    shannon_pass = password_strength(user_input)
    chat_gpt_pass = make_score_proportion(password_strength_chat_gpt(user_input))
    average_score = int(round(((shannon_pass + chat_gpt_pass) / 2), 2))
    result_rating = strength_rating(lang_state, average_score)

    text_tuple = (shannon_pass, chat_gpt_pass, average_score, result_rating)
    loop_trough_scores_tuple(strength_labels, text_tuple)

    return int(average_score)


def search_screen(
        lang_state: str,
        search_query: str,
        data_list: Dict[str, List[Tuple[int | str]]]
):
    search_window = CTkToplevel()
    search_window.title('Password Generator: search')
    search_window.geometry('700x385')
    search_window.minsize(700, 385)
    search_window.wait_visibility()
    search_window.grab_set()

    top_frame = CTkFrame(search_window)
    label = CTkLabel(
        top_frame, text=json_localization_data[lang_state]['toplevel_windows']['search_window_data'],
    )

    query_cell = CTkEntry(top_frame)
    query_cell.insert('end', search_query)
    query_cell.configure(state='disabled')

    table_frame = CTkFrame(search_window)
    data_for_table = SearchTable(table_frame, lang_state, 800, 500, 12)
    data_for_table.get_data_from_db(lang_state, data_list)

    label.pack(side='left', padx=10, pady=10)
    query_cell.pack(side='left', expand=True, fill='both', padx=10, pady=10)
    top_frame.pack(expand=True, fill='both', pady=(10, 0), padx=10)
    table_frame.pack(expand=True, fill='both', padx=10, pady=10)

    def on_close():
        search_window.destroy()
        search_window.quit()

    search_window.wm_protocol('WM_DELETE_WINDOW', on_close)

    search_window.mainloop()


def database_search(event: Any, lang_state: str) -> None:
    user_search = search_query_input_message(lang_state)

    if user_search is None:
        return
    elif user_search == '' or len(user_search) > MAX_SEARCH_QUERY_LENGTH:
        invalid_search_query_message(lang_state)
        return

    data_list = retrieve_data_for_build_table_interface(lang_state, column_number=3, user_query=user_search)
    print(data_list)

    if not data_list['data']:
        no_matches_for_search_message(lang_state, user_search)
        return

    # if data_list['data'].empty:
    #     no_matches_for_search_message(lang_state, user_search)
    #     return

    search_screen(lang_state, user_search, data_list)


def alphabet_screen(lang_state: str):
    alphabet_store_connector = AlphabetStore()

    alphabet_window = CTkToplevel()
    alphabet_window.title('Password Generator: alphabet')
    alphabet_window.geometry('700x300')
    alphabet_window.minsize(700, 300)
    alphabet_window.wait_visibility()
    alphabet_window.grab_set()

    letters_label = CTkLabel(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows']['alphabet_window_data']['labels']['letters_label']
    )
    letters_entry = CTkEntry(alphabet_window)

    digits_label = CTkLabel(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows']['alphabet_window_data']['labels']['digits_label']
    )
    digits_entry = CTkEntry(alphabet_window)

    punctuation_label = CTkLabel(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows'][
            'alphabet_window_data']['labels']['punctuation_label']
    )
    punctuation_entry = CTkEntry(alphabet_window)

    insert_alphabet_to_entries(alphabet_store_connector, letters_entry, digits_entry, punctuation_entry)

    quit_btn = CTkButton(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows']['alphabet_window_data']['buttons']['close'],
        command=lambda: alphabet_window.destroy()
    )

    save_alphabet_btn = CTkButton(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows'][
            'alphabet_window_data']['buttons']['save_alphabet_btn'],
        command=lambda: save_custom_alphabet(
            alphabet_store_connector, letters_entry, digits_entry, punctuation_entry
        )
    )

    reset_alphabet_btn = CTkButton(
        alphabet_window,
        text=json_localization_data[lang_state]['toplevel_windows'][
            'alphabet_window_data']['buttons']['reset_alphabet_btn'],
        command=lambda: back_to_default_alphabet(
            alphabet_store_connector, letters_entry, digits_entry, punctuation_entry
        )
    )

    letters_label.grid(row=0, column=0, padx=(30, 2), sticky='w')
    letters_entry.grid(row=0, column=1, columnspan=2, padx=(2, 30), sticky='we')

    digits_label.grid(row=1, column=0, padx=(30, 2), sticky='w')
    digits_entry.grid(row=1, column=1, columnspan=2, padx=(2, 30), sticky='we')

    punctuation_label.grid(row=2, column=0, padx=(30, 2), sticky='w')
    punctuation_entry.grid(row=2, column=1, columnspan=2, padx=(2, 30), sticky='we')

    quit_btn.grid(row=3, column=0, padx=10, sticky='we')
    save_alphabet_btn.grid(row=3, column=1, padx=10, sticky='we')
    reset_alphabet_btn.grid(row=3, column=2, padx=10, sticky='we')

    alphabet_window_column_number = alphabet_window.grid_size()[0]
    alphabet_window_row_number = alphabet_window.grid_size()[1]
    set_equal_grid_segments_size(alphabet_window, alphabet_window_column_number, alphabet_window_row_number)

    alphabet_window.mainloop()


def insert_alphabet_to_entries(
        db_connector: AlphabetStore,
        letter_entry: CTkEntry,
        digits_entry: CTkEntry,
        punctuation_entry: CTkEntry
):
    alphabet_data = db_connector.select_alphabet()

    if alphabet_data is not None:
        insert_to_entries(
            letter_entry, digits_entry, punctuation_entry, alphabet_data[1], alphabet_data[2], alphabet_data[3]
        )
    else:
        insert_to_entries(
            letter_entry, digits_entry, punctuation_entry, DEFAULT_LETTERS, DEFAULT_DIGITS, DEFAULT_PUNCTUATION
        )


def insert_to_entries(
        letter_entry: CTkEntry,
        digits_entry: CTkEntry,
        punctuation_entry: CTkEntry,
        digits_data: str,
        letters_data: str,
        punctuation_data: str,
):
    letter_entry.insert(0, digits_data)
    digits_entry.insert(0, letters_data)
    punctuation_entry.insert(0, punctuation_data)


def clear_entries(letter_entry: CTkEntry, digits_entry: CTkEntry, punctuation_entry: CTkEntry):
    letter_entry.delete(0, 'end')
    digits_entry.delete(0, 'end')
    punctuation_entry.delete(0, 'end')


def check_for_repeated_characters(user_input: str) -> bool:
    for char in user_input:
        if user_input.count(char) > 1:
            return False
    return True


def check_for_letters(user_input: str) -> bool:
    return user_input.isalpha()


def check_for_digits(user_input: str) -> bool:
    return user_input.isnumeric()


def check_for_punctuation(user_input: str) -> bool:
    if not user_input:
        return False

    for char in user_input:
        if char in NOT_ALLOWED_PUNCTUATION or char.isdigit() or char.isalpha() or char.isspace():
            return False
    return True


def save_custom_alphabet(
        db_connector: AlphabetStore,
        letter_entry: CTkEntry,
        digits_entry: CTkEntry,
        punctuation_entry: CTkEntry
):
    alphabet_data = db_connector.select_alphabet()

    new_letters = letter_entry.get()
    new_digits = digits_entry.get()
    new_punctuation = punctuation_entry.get()

    if not check_for_repeated_characters(new_letters) or \
            not check_for_repeated_characters(new_digits) or \
            not check_for_repeated_characters(new_punctuation):
        print('Repeated symbols detected!')
        return

    if not check_for_letters(new_letters):
        print('Invalid letter input!')
        return

    print(new_digits)

    if not check_for_digits(new_digits):
        print('Invalid digits input!')
        return

    if not check_for_punctuation(new_punctuation):
        print('Invalid punctuation input!')
        return

    if (alphabet_data is None) and (
            new_letters == DEFAULT_LETTERS and
            new_digits == DEFAULT_DIGITS and
            new_punctuation == DEFAULT_PUNCTUATION
    ):
        print('Fields are not changed! Its default values.')
    elif (alphabet_data is not None) and (
            new_letters == alphabet_data[1] and
            new_digits == alphabet_data[2] and
            new_punctuation == alphabet_data[3]
    ):
        print('Fields are the same that is was!')
    else:
        if alphabet_data is None:
            db_connector.insert_into_alphabet(new_letters, new_digits, new_punctuation)
        else:
            db_connector.update_alphabet(new_letters, new_digits, new_punctuation)


def back_to_default_alphabet(
        db_connector: AlphabetStore,
        letter_entry: CTkEntry,
        digits_entry: CTkEntry,
        punctuation_entry: CTkEntry
):
    alphabet_data = db_connector.select_alphabet()

    if (alphabet_data is None) or (
            (alphabet_data is not None) and (
            alphabet_data[1] == DEFAULT_LETTERS and
            alphabet_data[2] == DEFAULT_DIGITS and
            alphabet_data[3] == DEFAULT_PUNCTUATION)
    ):
        print('Already is default!')
    else:
        db_connector.update_alphabet(DEFAULT_LETTERS, DEFAULT_DIGITS, DEFAULT_PUNCTUATION)
        print('Set to default successfully!')

    clear_entries(letter_entry, digits_entry, punctuation_entry)
    insert_to_entries(
        letter_entry, digits_entry, punctuation_entry, DEFAULT_LETTERS, DEFAULT_DIGITS, DEFAULT_PUNCTUATION
    )


def set_equal_grid_segments_size(frame: CTkFrame | CTkToplevel, column_number: int, row_number: int):
    for column in range(column_number):
        frame.columnconfigure(column, weight=1, uniform='equal')
    for row in range(row_number):
        frame.rowconfigure(row, weight=1, uniform='equal')
