from tkinter.ttk import Treeview, Frame
from typing import Dict, List, Tuple

from .encryption_decryption import decrypt
from .treeview_processing import insert_table_data, treeview_scrollbars


def make_table_for_page_and_search(data: Dict[str, List[Tuple[int | str]]], tree: Treeview, main_frame: Frame):
    # pandas_table_iterator = data['data']
    # data_list_decrypted_column = pandas_table_iterator.iloc[:, 2].apply(decrypt)
    # pandas_table_iterator.iloc[:, 2] = data_list_decrypted_column

    data_list = data['data']
    # for row_index, row in enumerate(data_list):
    #     for column_index, column in enumerate(row):
    #         if column_index == 2:
    #             data_list[row_index][column_index] = decrypt(column)
    # print(data_list)

    decrypted_data_list = [
        [decrypt(column) if column_index == 2 else column for column_index, column in enumerate(row)]
        for row in data_list
    ]
    print(decrypted_data_list)

    table_header = data['localized_columns']
    tree['columns'] = table_header

    tree.column('#0', width=0, stretch=False)

    # insert_table_data(tree, table_header, pandas_table_iterator)
    insert_table_data(tree, table_header, decrypted_data_list)
    treeview_scrollbars(main_frame, tree)

    tree.pack()
