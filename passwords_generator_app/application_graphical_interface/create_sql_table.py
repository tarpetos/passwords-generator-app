import sqlite3

from tkinter.ttk import Entry, Treeview, Frame

from ..user_actions_processing.get_tables_columns_names import (
    retrieve_data_for_build_table_interface,
)
from ..user_actions_processing.encryption_decryption import encrypt
from ..user_actions_processing.make_table import make_table_for_page_and_search
from ..user_actions_processing.main_checks import (
    check_if_repeatable_characters_is_present,
)
from ..app_translation.messagebox_with_lang_change import (
    duplicate_description_message,
    successful_update_message,
)
from ..database_connections.password_store import PasswordStore


class TableBase:
    def __init__(self, root, lang_state, frame_width, frame_height, treeview_height):
        self.current_language = lang_state
        self.database_connector = PasswordStore()
        self.full_frame = Frame(root, width=frame_width, height=frame_height)
        self.full_frame.pack(side="top", fill="both", expand=True)

        self.data_list = None
        self.edit_cell_entry = None
        self.new_treeview_height = treeview_height
        self.new_treeview_cell_width = None

        self.table_tree_frame = Treeview(
            self.full_frame, height=treeview_height, style="TreeviewStyle.Treeview"
        )
        self.table_tree_frame.bind("<Double-1>", self.on_double_click)

        root.bind("<Configure>", self.on_window_resize)

    def get_data_from_db(self, lang_state, search_data_list=None):
        data_for_table = search_data_list if search_data_list else self.data_list
        make_table_for_page_and_search(
            data_for_table, self.table_tree_frame, self.full_frame
        )

    def on_double_click(self, event):
        region_clicked = self.table_tree_frame.identify_region(event.x, event.y)

        if region_clicked != "cell":
            return

        column_clicked = self.table_tree_frame.identify_column(event.x)
        column_index = int(column_clicked[1:]) - 1

        if column_index not in (1, 2):
            return

        selected_element_iid = self.table_tree_frame.focus()
        selected_text = self.table_tree_frame.item(selected_element_iid).get("values")[
            column_index
        ]

        column_box = self.table_tree_frame.bbox(selected_element_iid, column_clicked)

        self.edit_cell_entry = Entry(
            self.full_frame, width=column_box[2], style="EntryStyle.TEntry"
        )

        self.edit_cell_entry.editing_column_index = column_index
        self.edit_cell_entry.editing_item_iid = selected_element_iid

        self.edit_cell_entry.insert(0, selected_text)
        self.edit_cell_entry.select_range(0, "end")
        self.edit_cell_entry.focus()

        self.edit_cell_entry.bind("<FocusOut>", self.on_focus_out)
        self.edit_cell_entry.bind("<Return>", self.on_enter_pressed)

        self.edit_cell_entry.place(
            x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3]
        )

    def on_enter_pressed(self, event):
        new_text = event.widget.get()

        selected_iid = event.widget.editing_item_iid
        column_index = event.widget.editing_column_index

        current_values = self.table_tree_frame.item(selected_iid).get("values")
        saved_values = current_values.copy()
        current_values[column_index] = new_text
        modified_values = current_values

        self.update_table(selected_iid, current_values, saved_values, modified_values)

        event.widget.destroy()

    def update_table(self, selected_iid, current_values, saved_values, modified_values):
        table_connector = self.database_connector

        if saved_values != modified_values:
            self.insert_treeview_data_into_database(
                table_connector, modified_values, selected_iid, current_values
            )

    def insert_treeview_data_into_database(
        self, table_connector, modified_values, selected_iid, current_values
    ):
        try:
            table_connector.update_password_data_by_id(
                modified_values[1],
                encrypt(modified_values[2]),
                len(modified_values[2]),
                check_if_repeatable_characters_is_present(modified_values[2]),
                modified_values[0],
            )
            self.table_tree_frame.item(selected_iid, values=current_values)
            successful_update_message(self.current_language)
        except sqlite3.IntegrityError:
            duplicate_description_message(self.current_language)
            return

    def on_window_resize(self, event=None):
        widget_height = event.height
        widget_width = event.width
        self.new_treeview_height = int(widget_height / 21.6)
        self.table_tree_frame.configure(height=self.new_treeview_height)

        self.new_treeview_cell_width = int(widget_width / 2)

        for column in self.table_tree_frame["columns"]:
            self.table_tree_frame.column(
                column,
                minwidth=self.new_treeview_cell_width,
                width=self.new_treeview_cell_width,
            )

    @staticmethod
    def on_focus_out(event):
        event.widget.destroy()


class MainTable(TableBase):
    def __init__(
        self, root, lang_state, search_func, frame_width, frame_height, treeview_height
    ):
        self.current_language = lang_state
        super().__init__(
            root, self.current_language, frame_width, frame_height, treeview_height
        )

        self.data_list = retrieve_data_for_build_table_interface(lang_state)

        self.table_tree_frame.bind("<Control-f>", search_func)
        self.table_tree_frame.bind("<Control-F>", search_func)
        self.table_tree_frame.bind("<Enter>", lambda event: self.full_frame.focus_set())

    def reload_table(self, root, search_func, lang_state):
        self.full_frame.destroy()
        self.__init__(root, lang_state, search_func, 200, 200, self.new_treeview_height)
        self.get_data_from_db(lang_state)
        root.bind("Configure", self.on_window_resize)


class SearchTable(TableBase):
    def __init__(self, root, lang_state, frame_width, frame_height, treeview_height):
        self.current_language = lang_state
        super().__init__(
            root, self.current_language, frame_width, frame_height, treeview_height
        )


class HistoryTable(TableBase):
    def __init__(self, root, lang_state, frame_width, frame_height, treeview_height):
        self.current_language = lang_state
        super().__init__(
            root, self.current_language, frame_width, frame_height, treeview_height
        )

        self.data_list = retrieve_data_for_build_table_interface(
            lang_state, column_number=8
        )

    def get_data_from_db(self, lang_state, search_data_list=None):
        make_table_for_page_and_search(
            self.data_list, self.table_tree_frame, self.full_frame
        )

    def on_enter_pressed(self, event):
        pass
