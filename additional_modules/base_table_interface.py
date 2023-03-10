from tkinter import ttk

from customtkinter import CTkFrame

from additional_modules.make_table import make_table_for_page_and_search


class TableBase:
    def __init__(self, root,  frame_width, frame_height, treeview_height):
        self.full_frame = CTkFrame(root, width=frame_width, height=frame_height, fg_color='#34495E')
        self.full_frame.pack(side='top')

        self.data_list = None
        self.table_tree_frame = ttk.Treeview(self.full_frame, height=treeview_height)

    def get_data_from_db(self, lang_state, search_data_list=None):
        data_for_table = search_data_list if search_data_list else self.data_list
        make_table_for_page_and_search(lang_state, data_for_table, self.table_tree_frame, self.full_frame)
