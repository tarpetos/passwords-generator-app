import json

def load_json_localization_data():
    with open('localization.json') as translation_file:
        translation_data = json.load(translation_file)

        return translation_data


all_json_localization_data = load_json_localization_data()
