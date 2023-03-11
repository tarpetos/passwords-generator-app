from additional_modules.base_table_interface import TableBase
from create_app.inputs_and_buttons_processing import retrieve_data_for_build_table_interface
from create_app.store_user_passwords import PasswordStore


class TableInterface(TableBase):
    def __init__(self, root, lang_state, search_func, frame_width, frame_height, treeview_height):
        self.current_language = lang_state
        super().__init__(root, self.current_language, frame_width, frame_height, treeview_height, PasswordStore)

        self.data_list = retrieve_data_for_build_table_interface(lang_state)

        self.table_tree_frame.bind('<Control-f>', search_func)
        self.table_tree_frame.bind('<Control-F>', search_func)
        self.table_tree_frame.bind('<Enter>', lambda event: self.full_frame.focus_set())


    def reload_table(self, root, search_func, lang_state):
        self.full_frame.destroy()
        self.__init__(root, lang_state, search_func, 800, 430, 20)
        self.get_data_from_db(lang_state)
