from typing import Iterator, Any

from pandas import DataFrame

from ..app_translation.load_data_for_localization import all_json_localization_data
from ..database_connections.local_db_connection import PasswordStore


database_user_data = PasswordStore()


def table_column_names() -> tuple[list, list]:
    en_table_columns_names = [column for column in all_json_localization_data['EN']['table_column_names'].values()]
    uk_table_columns_names = [column for column in all_json_localization_data['UA']['table_column_names'].values()]

    return en_table_columns_names, uk_table_columns_names


def retrieve_data_for_build_table_interface(
        lang_state,
        column_number=5,
        user_query=None
) -> dict[str, list | Iterator[DataFrame] | DataFrame | Any]:
    column_name_localization = table_column_names()
    en_table_lst = column_name_localization[0][:column_number]
    uk_table_lst = column_name_localization[1][:column_number]

    if user_query:
        full_list_of_data = database_user_data.select_search_data_by_desc(user_query)
    else:
        full_list_of_data = database_user_data.select_full_table()

    return {'lang': lang_state, 'english_lst': en_table_lst, 'ukrainian_lst': uk_table_lst, 'data': full_list_of_data}
