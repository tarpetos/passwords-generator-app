from tkinter.constants import W, NO, CENTER, END
from tkinter.ttk import Scrollbar


def treeview_scrollbars(root, tree):
    vertical_scrollbar = Scrollbar(root, orient="vertical", command=tree.yview)
    vertical_scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vertical_scrollbar.set)

    horizontal_scrollbar = Scrollbar(root, orient="horizontal", command=tree.xview)
    horizontal_scrollbar.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=horizontal_scrollbar.set)


def insert_table_data(tree, table_header, pandas_iterator):
    for column_number, column in enumerate(tree["columns"]):
        tree.column(column, anchor=W, minwidth=500, width=500, stretch=NO)
        tree.heading(
            column,
            text=table_header[column_number],
            anchor=CENTER,
            command=lambda col=column_number: sort_column(tree, col, False),
        )

    print(pandas_iterator)
    # for row_number, row in enumerate(pandas_iterator.values):
    #     tree.insert('', END, text=str(row_number), values=row.tolist())

    for row_number, row in enumerate(pandas_iterator):
        tree.insert("", END, text=str(row_number), values=row)


def sort_column(tree, column, reverse):
    data = [(tree.set(child, column), child) for child in tree.get_children("")]

    key_func = lambda x: str(x[0]).lower()
    data.sort(key=key_func, reverse=reverse)

    for index, (_, child) in enumerate(data):
        tree.move(child, "", index)

    tree.heading(
        "#{}".format(column),
        command=lambda col=column: sort_column(tree, col, not reverse),
    )
