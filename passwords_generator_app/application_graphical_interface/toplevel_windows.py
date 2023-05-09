from typing import Dict, Iterator, Any

from customtkinter import (
    CTkLabel,
    CTkFrame,
    CTkEntry,
    CTk,
    CTkToplevel,
    CTkCanvas,
    CTkProgressBar,
    get_appearance_mode,
)

from tkinter import ttk, StringVar

from pandas import DataFrame

from .create_sql_table import retrieve_data_for_build_table_interface, SearchTable, HistoryTable
from .change_background_color import change_pop_up_color
from ..app_translation.load_data_for_localization import json_localization_data

from ..app_translation.messagebox_with_lang_change import (
    search_query_input_message,
    no_matches_for_search_message,
    invalid_search_query_message
)

from ..user_actions_processing.password_strength_score import (
    password_strength,
    make_score_proportion,
    strength_rating,
    password_strength_chat_gpt,
)

MAX_SEARCH_QUERY_LENGTH = 500


def app_loading_screen(lang_state) -> CTk:
    loading_screen = CTk()
    loading_screen.overrideredirect(True)
    loading_screen.eval('tk::PlaceWindow . center')
    loading_screen.title('Loading')
    loading_screen.geometry('400x100')
    loading_screen.wm_attributes('-alpha', 0.9)

    canvas = CTkCanvas(loading_screen, bg='#292929', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    load_label = CTkLabel(
        canvas, text=json_localization_data[lang_state]['toplevel_windows']['loading_window_data'],
        font=('Arial bold', 30), text_color='#D9D9D9', fg_color='#292929'
    )
    load_label.pack(pady=(30, 0))

    main_pop_up_bg = change_pop_up_color(canvas, load_label)
    canvas.create_rectangle(-1, -1, 400, 100, fill=main_pop_up_bg)

    loading_screen.update()

    return loading_screen


def generator_history_screen(lang_state):
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


def password_strength_screen(lang_state):
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

    def entry_modified(str_var):
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

    def update_rectangle(rating):
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


def strength_check(str_var_modifier, lang_state: str, strength_labels: tuple) -> int:
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
        data_list: Dict[str, list | Iterator[DataFrame] | DataFrame | Any]
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

    if data_list['data'].empty:
        no_matches_for_search_message(lang_state, user_search)
        return

    search_screen(lang_state, user_search, data_list)


def set_equal_grid_segments_size(frame: CTkFrame, column_number: int, row_number: int):
    for column in range(column_number):
        frame.columnconfigure(column, weight=1, uniform='equal')
    for row in range(row_number):
        frame.rowconfigure(row, weight=1, uniform='equal')
