import os
import sqlite3
from typing import AnyStr


def docker_check_path() -> AnyStr:
    return os.path.expanduser('~/.passwords/') if os.path.exists('/home/') else os.path.expanduser('passwords/')


ROOT_PATH = docker_check_path()


class LocalDatabaseConnector:
    def __init__(self):
        self.con = sqlite3.connect(f'{ROOT_PATH}data.db')
        self.cur = self.con.cursor()
