import os
import sqlite3
from typing import AnyStr


def docker_check_path() -> AnyStr:
    docker_is_active = os.environ.get("IS_DOCKER_ENV", False)
    print("Current dir: ", os.curdir)
    if docker_is_active:
        return "/root/password_generator/"
    else:
        return os.path.expanduser("~/.passwords/")


ROOT_PATH = docker_check_path()


class LocalDatabaseConnector:
    def __init__(self):
        db_path = os.path.join(ROOT_PATH, "data.db")
        print("Result path:", db_path)
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        self.con.commit()
