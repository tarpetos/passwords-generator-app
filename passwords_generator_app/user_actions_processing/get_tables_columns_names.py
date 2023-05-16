from typing import Iterator, Dict, List
from pandas import DataFrame

from ..database_connections.password_store import PasswordStore
from ..app_translation.load_data_for_localization import json_localization_data


database_user_data = PasswordStore()


def table_column_names(lang_state: str) -> List[str]:
    get_table_column_names = json_localization_data[lang_state]['table_column_names']

    return get_table_column_names


def retrieve_data_for_build_table_interface(
        lang_state: str,
        column_number: int = 5,
        user_query: str = None
) -> Dict[str, List[str] | Iterator[DataFrame] | DataFrame]:
    column_names_localized = table_column_names(lang_state)

    if column_number == 3:
        column_names_localized = column_names_localized[:3]
        full_list_of_data = database_user_data.select_search_data_by_desc(user_query)
    elif column_number == 5:
        column_names_localized = column_names_localized[:5]
        full_list_of_data = database_user_data.select_full_table()
    else:
        column_names_localized = column_names_localized[:3] + column_names_localized[5:]
        full_list_of_data = database_user_data.select_full_history_table()

    return {'localized_columns': column_names_localized, 'data': full_list_of_data}
