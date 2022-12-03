from tkinter import Text, Frame
from tkinter.constants import END, NONE, WORD

from tkscrolledframe import ScrolledFrame

from modules.inputs_and_buttons_validation import get_data_from_database_table


class CreateTable:
    def __init__(self, root):
        self.input_table_cell = None
        full_frame = ScrolledFrame(root, width=640, height=410)
        full_frame.pack(side="top")

        full_frame.bind_arrow_keys(root)
        full_frame.bind_scroll_wheel(root)
        self.inner_frame = full_frame.display_widget(Frame)

    def get_data_from_table(self):
        full_list_of_data = get_data_from_database_table()
        for tuple_row_element in range(len(full_list_of_data)):
            for tuple_column_elemnt in range(len(full_list_of_data[tuple_row_element])):
                self.input_table_cell = Text(
                    self.inner_frame,
                    width=14,
                    height=2,
                    wrap=NONE,
                    fg='black',
                    borderwidth=1.5,
                    font=('Arial', 9, 'bold'),
                )

                self.input_table_cell.grid(row=tuple_row_element, column=tuple_column_elemnt)
                self.input_table_cell.insert(END, full_list_of_data[tuple_row_element][tuple_column_elemnt])
                self.add_special_text_config(tuple_row_element, tuple_column_elemnt)

    def add_special_text_config(self, row_element, column_elemnt):
        if row_element == 0:
            self.input_table_cell.config(state='disabled', wrap=WORD, height=3, background='green', fg='white')

        if column_elemnt == 1 or column_elemnt == 2:
            self.input_table_cell.config(width=40)

        if (column_elemnt != 1 and column_elemnt != 2) and row_element != 0:
            self.input_table_cell.config(background='yellow', state='disabled')
