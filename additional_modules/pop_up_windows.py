from tkinter import Text, Canvas, Label
from tkinter.constants import NONE, END, WORD

import customtkinter
from customtkinter import CTkLabel, CTkFrame, CTkScrollbar, CTkCanvas, CTkTextbox

# from tkscrolledframe import ScrolledFrame

from additional_modules.encryption_decryption import decrypt
from change_interface_look.change_background_color import change_pop_up_color, change_search_box_color
from change_interface_look.wait_flowbox_style import round_rectangle


def app_loading_screen(lang_state):
    loading_screen = customtkinter.CTk()
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

def search_screen(lang_state, search_query, data_list):
    search_window = customtkinter.CTkToplevel()
    search_window.grab_set()
    search_window.title('Password Generator: search')
    search_window.geometry('700x400')
    search_window.resizable(False, False)

    search_frame = CTkFrame(search_window)

    table_frame = CTkFrame(search_frame)
    data_for_table = SearchTableInterface(table_frame)
    data_for_table.get_data_from_db(data_list)

    label = CTkLabel(
        search_frame,
        text=f'Search results for query: ' if lang_state else f'Результати пошуку на запит: ',
    )

    query_cell = Text(
        search_frame,
        height=1,
        wrap=NONE,
        fg='white',
        width=60,
        borderwidth=1.5,
        background='blue',
    )
    query_cell.insert(END, search_query)
    query_cell.config(state='disabled')

    label.grid(column=0, row=0, sticky='we', padx=(5, 0), pady=5)
    query_cell.grid(column=1, row=0, sticky='we', padx=(0, 5), pady=5)
    table_frame.grid(column=0, row=1, columnspan=2, sticky='nsew', pady=(0, 5))

    search_frame.pack(pady=10)
    # def on_close():
    #     search_window.destroy()
    #     search_window.quit()
    #
    # search_window.wm_protocol('WM_DELETE_WINDOW', on_close)

    search_window.mainloop()


class SearchTableInterface:
    def __init__(self, root):
        self.input_table_cell = None
        self.full_frame = CTkFrame(root, width=500, height=600)
        self.full_frame.pack(expand=True, fill='both')

        self.canvas = CTkCanvas(self.full_frame)
        change_search_box_color(self.canvas)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.table_frame = CTkFrame(self.canvas, width=self.canvas.winfo_reqwidth())
        self.table_frame.pack(side='top', fill='both', expand=True)

        self.v_scrollbar = CTkScrollbar(self.canvas, orientation='vertical', command=self.canvas.yview)
        self.v_scrollbar.pack(side='right', fill='y')

        self.h_scrollbar = CTkScrollbar(self.canvas, orientation='horizontal', command=self.canvas.xview)
        self.h_scrollbar.pack(side='bottom', fill='x')

        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

        self.table_frame.bind('<Configure>', self.adjust_canvas_scroll_region)

    def adjust_canvas_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def get_data_from_db(self, full_list_of_data):
        for tuple_row_element in range(len(full_list_of_data)):
            for tuple_column_element in range(len(full_list_of_data[tuple_row_element])):
                self.input_table_cell = CTkTextbox(
                    self.table_frame,
                    width=50,
                    height=40,
                    wrap=NONE,
                    corner_radius=0,
                    border_width=1,
                    font=('Arial', 16, 'bold'),

                )
                self.input_table_cell.grid(row=tuple_row_element, column=tuple_column_element)

                inserted_data_to_cell = full_list_of_data[tuple_row_element][tuple_column_element]
                if tuple_column_element == 2 and tuple_row_element != 0:
                    decrypted_password = decrypt(inserted_data_to_cell)
                    self.input_table_cell.insert(END, decrypted_password)
                else:
                    self.input_table_cell.insert(END, inserted_data_to_cell)

                self.add_special_text_config(tuple_row_element, tuple_column_element)

    def add_special_text_config(self, row_element, column_element):
        if column_element != 0:
            self.input_table_cell.configure(width=400)

        if row_element == 0:
            self.input_table_cell.configure(wrap=WORD, height=60, fg_color='green')
        else:
            self.input_table_cell.configure(height=40)
