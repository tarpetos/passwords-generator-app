import tkinter
from tkinter.constants import NONE, END, WORD
from tkinter.ttk import Label

from tkscrolledframe import ScrolledFrame

from additional_modules.encryption_decryption import decrypt
from change_interface_look.center_app import center_window
from change_interface_look.wait_flowbox_style import round_rectangle, load_screen_position_size


def app_loading_screen(main_window, lang_state):
    loading_screen = tkinter.Tk()
    loading_screen.overrideredirect(True)
    loading_screen.eval('tk::PlaceWindow . center')
    loading_screen.title('Loading')
    loading_screen.geometry('375x100')
    loading_screen.config(background='grey')
    loading_screen.attributes('-transparentcolor', 'grey')

    canvas = tkinter.Canvas(loading_screen, bg='grey', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    round_rectangle(0, 0, 375, 100, canvas, radius=70)

    load_screen_position_size(main_window, loading_screen)

    my_label = Label(
        canvas, text='Please wait...' if lang_state else 'Очікуйте, будь ласка...',
        font=('Arial bold', 24), foreground='white', background='black'
    )
    my_label.pack(pady=30)

    loading_screen.update()

    return loading_screen


def search_screen(lang_state, search_query, data_list):
    search_window = tkinter.Toplevel()
    search_window.grab_set()
    search_window.title('Password Generator: search')
    search_window.geometry('700x200')
    search_window.resizable(False, False)
    search_window.config(background='black')
    center_window(search_window)

    search_frame = tkinter.Frame(search_window, background='black')

    table_frame = tkinter.Frame(search_frame, background='black')
    data_for_table = SearchTableInterface(table_frame)
    data_for_table.get_data_from_db(data_list)

    label = Label(
        search_frame,
        text=f'Search results for query: ' if lang_state else f'Результати пошуку на запит: ',
        foreground='white',
        background='black',
        font=('Arial', 10, 'bold')
    )

    query_cell = tkinter.Text(
        search_frame,
        height=1,
        width=60,
        wrap=NONE,
        fg='black',
        borderwidth=1.5,
        background='red',
        font=('Arial', 10, 'bold'),
    )
    query_cell.insert(END, search_query)
    query_cell.config(state='disabled')

    label.grid(column=0, row=0, sticky='w')
    query_cell.grid(column=1, row=0, sticky='e')
    table_frame.grid(column=0, row=1, columnspan=2, sticky='nswe', pady=5)

    search_frame.pack(pady=15)

    search_window.mainloop()


class SearchTableInterface:
    def __init__(self, root):
        self.input_table_cell = None
        self.full_frame = ScrolledFrame(root, width=640, height=125)
        self.full_frame.pack(expand=True, fill='both')

        self.full_frame.bind_arrow_keys(root)
        self.full_frame.bind_scroll_wheel(root)

        self.inner_frame = self.full_frame.display_widget(tkinter.Frame)

    def get_data_from_db(self, full_list_of_data):
        for tuple_row_element in range(len(full_list_of_data)):
            for tuple_column_elemnt in range(len(full_list_of_data[tuple_row_element])):
                self.input_table_cell = tkinter.Text(
                    self.inner_frame,
                    width=9,
                    height=1,
                    wrap=NONE,
                    fg='black',
                    borderwidth=1.5,
                    font=('Arial', 9, 'bold'),
                )
                self.input_table_cell.grid(row=tuple_row_element, column=tuple_column_elemnt)

                iserted_data_to_cell = full_list_of_data[tuple_row_element][tuple_column_elemnt]
                if tuple_column_elemnt == 2 and tuple_row_element != 0:
                    decryped_password = decrypt(iserted_data_to_cell)
                    self.input_table_cell.insert(END, decryped_password)
                else:
                    self.input_table_cell.insert(END, iserted_data_to_cell)

                self.add_special_text_config(tuple_row_element, tuple_column_elemnt)


    def add_special_text_config(self, row_element, column_element):
        if column_element != 0:
            self.input_table_cell.config(width=40)

        if row_element == 0:
            self.input_table_cell.config(wrap=WORD, height=3, background='green', fg='white', state='disabled')
        else:
            self.input_table_cell.config(height=1, background='yellow', state='disabled')
