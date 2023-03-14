from customtkinter import (
    CTkLabel,
    CTkFrame,
    CTkEntry,
    CTk,
    CTkToplevel,
    CTkCanvas,
    CTkProgressBar,
    get_appearance_mode,
    CTkTextbox
)

from tkinter import ttk, StringVar

from .create_sql_table import retrieve_data_for_build_table_interface, SearchTableInterface, HistoryTableInterface
from .change_background_color import change_pop_up_color

from ..app_translation.messagebox_with_lang_change import (
    search_query_input_message,
    no_matches_for_search_message,
    invalid_search_query_message
)

from ..user_actions_processing.main_checks import MAX_AUTO_PASSWORD_AND_DESC_LENGTH
from ..user_actions_processing.password_strength_score import (
    password_strength,
    make_score_proportion,
    strength_rating,
    password_strength_chat_gpt,
)


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
        canvas, text='Please wait...' if lang_state else 'Очікуйте, будь ласка...',
        font=('Arial bold', 30), text_color='#D9D9D9', fg_color='#292929'
    )
    load_label.pack(pady=(30, 0))

    main_pop_up_bg = change_pop_up_color(canvas, load_label)
    canvas.create_rectangle(-1, -1, 400, 100, fill=main_pop_up_bg)

    loading_screen.update()

    return loading_screen


def generator_history_screen(lang_state):
    history_window = CTkToplevel()
    history_window.grab_set()
    history_window.title('Password Generator: generation history')
    history_window.geometry('900x502')
    history_window.resizable(False, False)

    history_frame = CTkFrame(history_window)

    info_textbox = CTkTextbox(history_frame, width=600, height=50)
    info_textbox.insert(
        'end',
        text=''
        'This table is updated automatically. When the number of records reaches 5000, then the oldest 2500 among '
        'all records will be deleted. Changes to this table have no effect on the main table.'
        if lang_state else
        'Ця таблиця оновлюється автоматично. Коли кількість записів досягає 5000, то 2500 старіших серед усіх записів '
        'будуть видалені. Зміни в цій таблиці ніяк не впливають на головну таблицю.'
    )
    info_textbox.configure(wrap='word', state='disabled')

    info_textbox.pack(side='top', expand=True, fill='both')

    data_for_table = HistoryTableInterface(history_frame, lang_state, 200, 200, 20)
    data_for_table.get_data_from_db(lang_state)

    history_frame.pack(pady=10, padx=10)

    history_window.mainloop()


def password_strength_screen(lang_state):
    strength_window = CTkToplevel()
    strength_window.grab_set()
    strength_window.title('Password Generator: strength checker')
    strength_window.geometry('700x350')
    strength_window.resizable(False, False)

    strength_frame = CTkFrame(strength_window)

    enter_label = CTkLabel(
        strength_frame,
        text='Enter password that you want to check for strength: '
        if lang_state else 'Введіть пароль, який ви хочете перевірити на надійність: ',
    )

    shanon_score_label = CTkLabel(
        strength_frame,
        text='Score on a scale from 0 to 100 (Shannon Entropy): '
        if lang_state else 'Оцінка по шкалі від 0 до 100 (Ентропія Шенона): '
    )

    ai_score_label = CTkLabel(
        strength_frame,
        text='Score on a scale from 0 to 100 (ChatGPT Algorithm): '
        if lang_state else 'Оцінка по шкалі від 0 до 100 (Алгоритм ChatGPT): '
    )

    average_score_label = CTkLabel(
        strength_frame,
        text='Average score: '
        if lang_state else 'Середній показник: '
    )

    reliability_label = CTkLabel(
        strength_frame,
        text='Reliability level: '
        if lang_state else 'Рівень надійності: '
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

    enter_label.grid(column=0, row=0, sticky='w', padx=10, pady=(20, 10))
    password_input_entry.grid(column=1, row=0, sticky='we', padx=(0, 10), pady=(20, 10))
    separator.grid(column=0, row=1, columnspan=2, sticky='we', padx=10, pady=(0, 10))

    shanon_score_label.grid(column=0, row=2, sticky='w', pady=10, padx=10)
    shanon_score_value_label.grid(column=1, row=2, sticky='w', pady=10)
    ai_score_label.grid(column=0, row=3, sticky='w', pady=10, padx=10)
    ai_score_value_label.grid(column=1, row=3, sticky='w', pady=10)
    average_score_label.grid(column=0, row=4, sticky='w', pady=10, padx=10)
    average_score_value_label.grid(column=1, row=4, sticky='w', pady=10)
    reliability_label.grid(column=0, row=5, sticky='w', pady=10, padx=10)
    reliability_value_label.grid(column=1, row=5, sticky='w', pady=10)

    strength_bar.grid(column=0, row=6, columnspan=2, sticky='we', pady=(30, 20), padx=50)

    strength_bar.update_idletasks()

    strength_frame.pack(pady=10, padx=10)

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


def strength_check(str_var_modifier, lang_state: bool, strength_labels: tuple) -> int:
    user_input = str_var_modifier.get()

    if not user_input:
        loop_trough_scores_tuple(strength_labels)
        return 0

    shannon_pass = password_strength(user_input)
    chat_gpt_pass = make_score_proportion(password_strength_chat_gpt(user_input))
    average_score = round(((shannon_pass + chat_gpt_pass) / 2), 2)
    result_rating = strength_rating(lang_state, average_score)

    text_tuple = (shannon_pass, chat_gpt_pass, average_score, result_rating)
    loop_trough_scores_tuple(strength_labels, text_tuple)

    return int(average_score)


def search_screen(lang_state, search_query, data_list):
    search_window = CTkToplevel()
    search_window.grab_set()
    search_window.title('Password Generator: search')
    search_window.geometry('700x385')
    search_window.resizable(False, False)

    search_frame = CTkFrame(search_window)

    table_frame = CTkFrame(search_frame)
    data_for_table = SearchTableInterface(table_frame, lang_state, 800, 500, 12)
    data_for_table.get_data_from_db(lang_state, data_list)

    label = CTkLabel(
        search_frame, text='Search results for query: ' if lang_state else 'Результати пошуку на запит: ',
    )

    query_cell = CTkEntry(search_frame)
    query_cell.insert('end', search_query)
    query_cell.configure(state='disabled')

    label.grid(column=0, row=0, sticky='w', padx=10, pady=10)
    query_cell.grid(column=1, row=0, sticky='we', padx=10, pady=10)
    table_frame.grid(column=0, row=1, columnspan=2, sticky='we', pady=10, padx=10)

    search_frame.columnconfigure(0, weight=1, uniform='equal')
    search_frame.columnconfigure(1, weight=1, uniform='equal')
    search_frame.pack(pady=20, padx=10)

    def on_close():
        search_window.destroy()
        search_window.quit()

    search_window.wm_protocol('WM_DELETE_WINDOW', on_close)

    search_window.mainloop()


def database_search(event, lang_state):
    user_search = search_query_input_message(lang_state)

    if user_search is None:
        return
    elif user_search == '' or len(user_search) > MAX_AUTO_PASSWORD_AND_DESC_LENGTH:
        invalid_search_query_message(lang_state)
        return

    data_list = retrieve_data_for_build_table_interface(lang_state, column_number=3, user_query=user_search)

    if data_list['data'].empty:
        no_matches_for_search_message(lang_state, user_search)
        return

    search_screen(lang_state, user_search, data_list)
