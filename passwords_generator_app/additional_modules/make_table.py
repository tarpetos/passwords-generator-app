from ..additional_modules.encryption_decryption import decrypt
from ..additional_modules.treeview_processing import get_table_col_header, insert_table_data, treeview_scrollbars


def make_table_for_page_and_search(lang_state, data, tree, main_frame):
    pandas_table_iterator = data['data']
    data_list_decrypted_column = pandas_table_iterator.iloc[:, 2].apply(decrypt)
    pandas_table_iterator.iloc[:, 2] = data_list_decrypted_column

    tree['columns'] = list(pandas_table_iterator.columns)

    tree.column('#0', width=0, stretch='no')

    table_header = get_table_col_header(lang_state, data)
    insert_table_data(tree, table_header, pandas_table_iterator)
    treeview_scrollbars(main_frame, tree)

    tree.pack()
