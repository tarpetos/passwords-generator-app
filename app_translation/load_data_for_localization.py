from typing import Any
import json

LOCALIZATION_FILE_PATH = './localization.json'


def load_json_data(file_path: str) -> Any:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


localization_data = load_json_data(LOCALIZATION_FILE_PATH)
