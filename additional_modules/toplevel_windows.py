from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTk, CTkToplevel

from tkinter import Canvas, Label, ttk, StringVar

from additional_modules.base_table_interface import TableBase
from additional_modules.password_strength_score import password_strength, make_score_proportion, strength_rating, \
    password_strength_chat_gpt
from change_interface_look.change_background_color import change_pop_up_color
from change_interface_look.wait_flowbox_style import round_rectangle
from create_app.store_user_passwords import PasswordStore


def app_loading_screen(lang_state) -> CTk:
    loading_screen = CTk()
    loading_screen.overrideredirect(True)
    loading_screen.eval('tk::PlaceWindow . center')
    loading_screen.title('Loading')
    loading_screen.geometry('400x100')

    canvas = Canvas(loading_screen, bg='#292929', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    load_label = Label(
        canvas, text='Please wait...' if lang_state else 'Очікуйте, будь ласка...',
        font=('Arial bold', 24), foreground='#D9D9D9', background='#292929'
    )
    load_label.pack(pady=30)

    main_pop_up_bg = change_pop_up_color(canvas, load_label)
    round_rectangle(0, 0, 400, 100, canvas, main_pop_up_bg, radius=70)

    loading_screen.update()

    return loading_screen


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

    canvas = Canvas(strength_frame, height=20, background='gray', highlightthickness=0)

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
    canvas.grid(column=0, row=6, columnspan=2, sticky='we', pady=(30, 20), padx=50)
    canvas.update_idletasks()
    canvas_width = canvas.winfo_width()

    strength_frame.pack(pady=10, padx=10)

    inner_rect = canvas.create_rectangle(0, 0, 0, 20, fill='red', outline='')

    def update_rectangle(rating):
        inner_rect_width = int(canvas_width * rating / 100)
        canvas.coords(inner_rect, 0, 0, inner_rect_width, 20)
        gradient = ['#FF0000', '#FF4D00', '#FF9900', '#FFFF00', '#BFFF00', '#00FF00']
        color_index = int(inner_rect_width / canvas_width * (len(gradient)))
        color_index = min(color_index, 5)
        color = gradient[color_index]
        canvas.itemconfigure(inner_rect, fill=color)

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


class SearchTableInterface(TableBase):
    def __init__(self, root, lang_state, frame_width, frame_height, treeview_height):
        self.current_language = lang_state
        super().__init__(root, self.current_language, frame_width, frame_height, treeview_height, PasswordStore)
