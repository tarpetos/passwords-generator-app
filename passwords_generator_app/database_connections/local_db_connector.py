import sqlite3

from ..app_translation.load_data_for_localization import ROOT_PATH


class LocalDatabaseConnector:
    def __init__(self):
        self.con = sqlite3.connect(f'{ROOT_PATH}data.db')
        self.cur = self.con.cursor()
