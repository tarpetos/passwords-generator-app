import sqlite3

from additional_modules.base_table_interface import TableBase
from additional_modules.encryption_decryption import encrypt
from app_translation.messagebox_with_lang_change import invalid_password_usage_message, invalid_password_value_message
from create_app.inputs_and_buttons_processing import \
    check_if_repeatable_characters_is_present, update_record_in_table, duplicate_usage_in_table, \
    nothing_to_update_in_table, successful_update_in_table, retrieve_data_for_build_table_interface
from create_app.store_user_passwords import PasswordStore


class TableInterface(TableBase):
    def __init__(self, root, lang_state, search_func, frame_width, frame_height, treeview_height):
        super().__init__(root, frame_width, frame_height, treeview_height)
        # self.data_from_storage = PasswordStore()
        # self.input_table_cell = None
        # self.table_header = None

        self.data_list = retrieve_data_for_build_table_interface(lang_state)

        self.table_tree_frame.bind('<Control-f>', search_func)
        self.table_tree_frame.bind('<Control-F>', search_func)
        self.table_tree_frame.bind('<Enter>', lambda event: self.full_frame.focus_set())

        # self.text_cells_list = []


    def reload_table(self, root, search_func, lang_state):
        self.full_frame.destroy()
        self.__init__(root, lang_state, search_func, 800, 430, 20)
        self.get_data_from_db(lang_state)

    def update_data_using_table_interface(self, lang_state):
        pass
        # update_id = self.data_from_storage.select_id()
        # data_for_compare = self.data_from_storage.select_descriptions_password()
        # data_list_from_user = self.text_cells_list
        #
        # search_for_update_flag = False
        #
        # data_list_for_check_length = len(data_list_from_user)
        #
        # try:
        #     for num_elem_in_list in range(data_list_for_check_length):
        #         table_id_for_update = update_id[num_elem_in_list][0]
        #         password_usage_cell_element = data_list_from_user[num_elem_in_list][0].get('1.0', 'end-1c')
        #         password_cell_element = data_list_from_user[num_elem_in_list][1].get('1.0', 'end-1c')
        #         encrypted_password = encrypt(password_cell_element)
        #         compare_with_usage = data_for_compare[num_elem_in_list][0]
        #         compare_with_password = data_for_compare[num_elem_in_list][1]
        #
        #         if password_usage_cell_element == '':
        #             invalid_password_usage_message(lang_state)
        #             return
        #         elif password_cell_element == '':
        #             invalid_password_value_message(lang_state)
        #             return
        #
        #         if compare_with_usage == password_usage_cell_element and compare_with_password == encrypted_password:
        #             continue
        #         else:
        #             if not search_for_update_flag and update_record_in_table(lang_state):
        #                 search_for_update_flag = True
        #                 self.data_from_storage.update_password_data_by_id(
        #                     password_usage_cell_element,
        #                     encrypted_password,
        #                     len(password_cell_element),
        #                     check_if_repeatable_characters_is_present(password_cell_element),
        #                     table_id_for_update,
        #                 )
        #                 successful_update_in_table(lang_state)
        #             elif search_for_update_flag:
        #                 self.data_from_storage.update_password_data_by_id(
        #                     password_usage_cell_element,
        #                     encrypted_password,
        #                     len(password_cell_element),
        #                     check_if_repeatable_characters_is_present(password_cell_element),
        #                     table_id_for_update,
        #                 )
        #             else:
        #                 return
        # except sqlite3.IntegrityError:
        #     duplicate_usage_in_table(lang_state)
        #     return
        #
        # if not search_for_update_flag:
        #     nothing_to_update_in_table(lang_state)
