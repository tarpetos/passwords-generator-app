from .encryption_decryption import decrypt
from .treeview_processing import insert_table_data, treeview_scrollbars


def make_table_for_page_and_search(data, tree, main_frame):
    pandas_table_iterator = data['data']
    data_list_decrypted_column = pandas_table_iterator.iloc[:, 2].apply(decrypt)
    pandas_table_iterator.iloc[:, 2] = data_list_decrypted_column

    table_header = data['localized_columns']
    tree['columns'] = table_header

    tree.column('#0', width=0, stretch='no')

    insert_table_data(tree, table_header, pandas_table_iterator)
    treeview_scrollbars(main_frame, tree)

    tree.pack()
