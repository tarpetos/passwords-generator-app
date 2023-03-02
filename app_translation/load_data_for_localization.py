import json

def load_json_localization_data():
    with open('localization.json') as translation_file:
        translation_data = json.load(translation_file)

        return translation_data


all_json_localization_data = load_json_localization_data()
en_table_columns_names = [column for column in all_json_localization_data['EN']['table_column_names'].values()]
uk_table_columns_names = [column for column in all_json_localization_data['UA']['table_column_names'].values()]
