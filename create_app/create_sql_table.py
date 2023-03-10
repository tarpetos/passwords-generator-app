import sqlite3
from tkinter import Text, Frame
from tkinter.constants import END, NONE, WORD, TOP

from tkscrolledframe import ScrolledFrame

from additional_modules.encryption_decryption import decrypt, encrypt
from app_translation.messagebox_with_lang_change import ivalid_password_usage_message, invalid_password_value_message
from create_app.inputs_and_buttons_processing import get_data_from_database_table, \
    check_if_repeatable_characters_is_present, update_record_in_table, duplicate_usage_in_table, \
    nothing_to_update_in_table, successful_update_in_table
from create_app.store_user_passwords import PasswordStore


get_data = PasswordStore()


class TableInterface:
    def __init__(self, root):
        self.input_table_cell = None
        self.full_frame = ScrolledFrame(root, width=640, height=410)
        self.full_frame.pack(side=TOP)

        self.full_frame.bind_arrow_keys(root)
        self.full_frame.bind_scroll_wheel(root)

        self.inner_frame = self.full_frame.display_widget(Frame)
        self.text_cells_list = []

    def get_data_from_db(self):
        self.remake_inner_frame()
        full_list_of_data = get_data_from_database_table()
        self.text_cells_list = []
        for tuple_row_element in range(len(full_list_of_data)):
            text_cells_rows = []
            for tuple_column_element in range(len(full_list_of_data[tuple_row_element])):
                self.input_table_cell = Text(
                    self.inner_frame,
                    width=14,
                    height=1,
                    wrap=NONE,
                    fg='black',
                    borderwidth=1.5,
                    font=('Arial', 9, 'bold'),
                )
                self.input_table_cell.grid(row=tuple_row_element, column=tuple_column_element)

                inserted_data_to_cell = full_list_of_data[tuple_row_element][tuple_column_element]
                if tuple_column_element == 2 and tuple_row_element != 0:
                    decrypted_password = decrypt(inserted_data_to_cell)
                    self.input_table_cell.insert(END, decrypted_password)
                else:
                    self.input_table_cell.insert(END, inserted_data_to_cell)
                self.add_special_text_config(tuple_row_element, tuple_column_element)

                if (1 <= tuple_column_element <= 2) and tuple_row_element != 0:
                    text_cells_rows.append(self.input_table_cell)

            if tuple_row_element != 0:
                self.text_cells_list.append(text_cells_rows)

        return self.text_cells_list

    def remake_inner_frame(self):
        self.full_frame.erase()
        self.inner_frame = self.full_frame.display_widget(Frame)

    def add_special_text_config(self, row_element, column_element):
        if row_element == 0:
            self.input_table_cell.config(wrap=WORD, height=3, background='green', fg='white', state='disabled')

        if column_element == 1 or column_element == 2:
            self.input_table_cell.config(width=40)

        if (column_element != 1 and column_element != 2) and row_element != 0:
            self.input_table_cell.config(background='yellow', state='disabled')

    def update_data_using_table_interface(self, lang_state):
        update_id = get_data.select_id()
        data_for_compare = get_data.select_descriptions_password()
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
                    ivalid_password_usage_message(lang_state)
                    return
                elif password_cell_element == '':
                    invalid_password_value_message(lang_state)
                    return

                if compare_with_usage == password_usage_cell_element and compare_with_password == encrypted_password:
                    continue
                else:
                    if not search_for_update_flag and update_record_in_table():
                        search_for_update_flag = True
                        get_data.update_password_data_by_id(
                            password_usage_cell_element,
                            encrypted_password,
                            len(password_cell_element),
                            check_if_repeatable_characters_is_present(password_cell_element),
                            table_id_for_update,
                        )
                        successful_update_in_table()
                    elif search_for_update_flag:
                        get_data.update_password_data_by_id(
                            password_usage_cell_element,
                            encrypted_password,
                            len(password_cell_element),
                            check_if_repeatable_characters_is_present(password_cell_element),
                            table_id_for_update,
                        )
                    else:
                        return
        except sqlite3.IntegrityError:
            duplicate_usage_in_table()
            return

        if not search_for_update_flag:
            nothing_to_update_in_table()