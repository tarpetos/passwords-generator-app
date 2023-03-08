import sqlite3

from customtkinter import CTkFrame, CTkScrollbar
from tkinter import ttk
from tkinter.constants import END, WORD, TOP, NO, CENTER, W

from additional_modules.encryption_decryption import decrypt, encrypt
from app_translation.messagebox_with_lang_change import invalid_password_usage_message, invalid_password_value_message
from create_app.inputs_and_buttons_processing import get_data_from_database_table, \
    check_if_repeatable_characters_is_present, update_record_in_table, duplicate_usage_in_table, \
    nothing_to_update_in_table, successful_update_in_table
from create_app.store_user_passwords import PasswordStore


class TableInterface:
    def __init__(self, root, search_func):
        self.data_from_storage = PasswordStore()
        self.input_table_cell = None
        self.pandas_table_iterator = None
        self.table_header = None

        self.full_frame = CTkFrame(root, width=800, height=430, fg_color='white')
        self.full_frame.pack(side=TOP)

        self.table_tree_frame = ttk.Treeview(self.full_frame, height=20)
        self.table_tree_frame.bind('<Control-f>', search_func)
        self.table_tree_frame.bind('<Control-F>', search_func)
        self.table_tree_frame.bind('<Enter>', lambda event: self.full_frame.focus_set())

        self.text_cells_list = []

    def get_data_from_db(self, lang_state):
        data_for_table = get_data_from_database_table(lang_state)
        self.pandas_table_iterator = data_for_table['data']
        data_list_decrypted_column = self.pandas_table_iterator.iloc[:, 2].apply(decrypt)
        self.pandas_table_iterator.iloc[:, 2] = data_list_decrypted_column

        self.table_tree_frame['columns'] = list(self.pandas_table_iterator.columns)

        self.table_tree_frame.column('#0', width=0, stretch=NO)

        self.table_header = self.get_table_col_header(lang_state, data_for_table)
        self.insert_table_data(self.table_header)

        vertical_scrollbar = CTkScrollbar(
            self.full_frame, orientation='vertical', command=self.table_tree_frame.yview
        )
        vertical_scrollbar.pack(side='right', fill='y')
        self.table_tree_frame.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = CTkScrollbar(
            self.full_frame, orientation='horizontal', command=self.table_tree_frame.xview
        )
        horizontal_scrollbar.pack(side='bottom', fill='x')
        self.table_tree_frame.configure(xscrollcommand=horizontal_scrollbar.set)
        self.table_tree_frame.pack()

    def insert_table_data(self, table_header):
        for column_number, column in enumerate(self.table_tree_frame['columns']):
            self.table_tree_frame.column(column, anchor=W, minwidth=300, width=300, stretch=NO)
            self.table_tree_frame.heading(column, text=table_header[column_number], anchor=CENTER)

        for row_number, row in enumerate(self.pandas_table_iterator.values):
            self.table_tree_frame.insert('', END, text=str(row_number), values=row.tolist())

    @staticmethod
    def get_table_col_header(lang_state, col_names) -> dict:
        return col_names['english_lst'] if lang_state else col_names['ukrainian_lst']

    def reload_table(self, root, search_func, lang_state):
        self.full_frame.destroy()
        self.__init__(root, search_func)
        self.get_data_from_db(lang_state)

    def add_special_config_to_text(self, row_element, column_element):
        if row_element == 0:
            self.input_table_cell.config(wrap=WORD, height=3, background='green', fg='white', state='disabled')

        if column_element == 1 or column_element == 2:
            self.input_table_cell.config(width=40)

        if (column_element != 1 and column_element != 2) and row_element != 0:
            self.input_table_cell.config(background='yellow', state='disabled')

    def update_data_using_table_interface(self, lang_state):
        update_id = self.data_from_storage.select_id()
        data_for_compare = self.data_from_storage.select_descriptions_password()
        data_list_from_user = self.text_cells_list

        search_for_update_flag = False

        data_list_for_check_length = len(data_list_from_user)

        try:
            for num_elem_in_list in range(data_list_for_check_length):
                table_id_for_update = update_id[num_elem_in_list][0]
                password_usage_cell_element = data_list_from_user[num_elem_in_list][0].get('1.0', 'end-1c')
                password_cell_element = data_list_from_user[num_elem_in_list][1].get('1.0', 'end-1c')
                encrypted_password = encrypt(password_cell_element)
                compare_with_usage = data_for_compare[num_elem_in_list][0]
                compare_with_password = data_for_compare[num_elem_in_list][1]

                if password_usage_cell_element == '':
                    invalid_password_usage_message(lang_state)
                    return
                elif password_cell_element == '':
                    invalid_password_value_message(lang_state)
                    return

                if compare_with_usage == password_usage_cell_element and compare_with_password == encrypted_password:
                    continue
                else:
                    if not search_for_update_flag and update_record_in_table(lang_state):
                        search_for_update_flag = True
                        self.data_from_storage.update_password_data_by_id(
                            password_usage_cell_element,
                            encrypted_password,
                            len(password_cell_element),
                            check_if_repeatable_characters_is_present(password_cell_element),
                            table_id_for_update,
                        )
                        successful_update_in_table(lang_state)
                    elif search_for_update_flag:
                        self.data_from_storage.update_password_data_by_id(
                            password_usage_cell_element,
                            encrypted_password,
                            len(password_cell_element),
                            check_if_repeatable_characters_is_present(password_cell_element),
                            table_id_for_update,
                        )
                    else:
                        return
        except sqlite3.IntegrityError:
            duplicate_usage_in_table(lang_state)
            return

        if not search_for_update_flag:
            nothing_to_update_in_table(lang_state)
