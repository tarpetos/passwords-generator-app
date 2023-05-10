import os
from typing import Any, Iterable
import sqlite3

PASSWORD_STORE_QUERIES = {
    'create_passwords_table':
        '''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description VARCHAR(384) NOT NULL,
            password VARCHAR(384) NOT NULL,
            length INTEGER NOT NULL,
            has_repeatable BOOLEAN NOT NULL,
            CONSTRAINT unique_data UNIQUE(description)
        )
        ''',
    'drop_passwords_table': 'DROP TABLE IF EXISTS passwords',
    'create_token_table':
        '''
        CREATE TABLE IF NOT EXISTS id_token (
            saved_id INTEGER NOT NULL,
            saved_token VARCHAR(384) NOT NULL
        )
        ''',
    'insert_password':
        '''
        INSERT OR IGNORE INTO passwords(description, password, length, has_repeatable)
        VALUES (?, ?, ?, ?)
        ''',
    'change_password':
        '''
        REPLACE INTO passwords(description, password, length, has_repeatable)
        VALUES (?, ?, ?, ?)
        ''',
    'change_token_data':
        '''
        INSERT INTO id_token(saved_id, saved_token)
        VALUES (?, ?)
        ''',
    'delete_token_data': 'DELETE FROM id_token',
    'get_first_token': 'SELECT * FROM id_token LIMIT 1',
    'change_password_by_id':
        '''
        UPDATE passwords
        SET description =  ?, password =  ?, length =  ?, has_repeatable =  ?
        WHERE id =  ?
        ''',
    'change_password_by_description':
        '''
        UPDATE passwords
        SET password =  ?, length =  ?, has_repeatable =  ?
        WHERE description =  ?
        ''',
    'fetch_passwords_descriptions':
        '''
        SELECT description FROM passwords
        ORDER BY id
        ''',
    'fetch_passwords_by_description':
        '''
        SELECT * FROM passwords
        WHERE LOWER(description) LIKE '%' || LOWER(?) || '%'
        ORDER BY id
        ''',
    'fetch_passwords': 'SELECT * FROM passwords',
    'fetch_passwords_ids':
        '''
        SELECT id FROM passwords
        ORDER BY id
        ''',
    'fetch_passwords_no_ids':
        '''
        SELECT description, password, length, has_repeatable FROM passwords
        ORDER BY id
        ''',
    'delete_password':
        '''
        DELETE FROM passwords
        WHERE id =  ?
        ''',
}


class PasswordStore:
    PASSWORDS_DIR = './.passwords/'
    PASSWORDS_DATA_FILE_NAME = 'data'

    def __init__(self):
        self.create_passwords_directory()
        self.con = sqlite3.connect(self.PASSWORDS_DIR + self.PASSWORDS_DATA_FILE_NAME)
        self.cur = self.con.cursor()

    def create_passwords_directory(self) -> None:
        if not os.path.exists(self.PASSWORDS_DIR):
            os.mkdir(self.PASSWORDS_DIR)

    def create_passwords_table(self) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['create_passwords_table'])

    def drop_passwords_table(self) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['drop_passwords_table'])

    def create_token_table(self) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['create_token_table'])

    def insert_password(self, description: str, password: str, length: int, repeatable: bool) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['insert_password'], description, password, length, repeatable)

    def change_password(self, description: str, password: str, length: int, repeatable: bool) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['change_password'], description, password, length, repeatable)

    def change_token_data(self, user_id: str, token: str) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['change_token_data'], user_id, token)

    def delete_token_data(self) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['delete_token_data'])

    def fetch_token_data(self) -> tuple[str]:
        token_data = self.read_query(PASSWORD_STORE_QUERIES['select_token_data'])
        if not token_data:
            raise ValueError('No records')
        first_record = token_data[0]
        return first_record

    def change_password_by_id(self, id: int, description: str, password: str, length: int, repeatable: bool) -> None:
        self.execute_query(
            PASSWORD_STORE_QUERIES['change_password_by_id'], description, password, length, repeatable, id
        )

    def change_password_by_description(self, description: str, password: str, length: int, repeatable: bool) -> None:
        self.execute_query(
            PASSWORD_STORE_QUERIES['change_password_by_description'], password, length, repeatable, description
        )

    def fetch_passwords_descriptions(self) -> list[tuple[str]]:
        password_descriptions = self.read_query(PASSWORD_STORE_QUERIES['fetch_passwords_descriptions'])
        return [
            password_description
            for (password_description,) in password_descriptions
        ]

    def fetch_passwords_by_description(self, description: str) -> list[tuple[Any]]:
        return self.read_query(PASSWORD_STORE_QUERIES['fetch_passwords_by_description'], description)

    def fetch_passwords(self) -> list[tuple[Any, ...]]:
        return self.read_query(PASSWORD_STORE_QUERIES['fetch_passwords'])

    def fetch_passwords_ids(self) -> list[int]:
        return [
            id
            for (id,) in self.read_query(PASSWORD_STORE_QUERIES['fetch_passwords_ids'])
        ]

    def fetch_passwords_no_ids(self) -> list[tuple[Any]]:
        return self.read_query(PASSWORD_STORE_QUERIES['fetch_passwords_no_ids'])

    def delete_password(self, id: int) -> None:
        self.execute_query(PASSWORD_STORE_QUERIES['delete_password'], id)

    def read_query(self, query: str, *options) -> list[tuple[Any]]:
        self.cur.execute(query, options)
        result = self.cur.fetchall()
        self.con.commit()
        return result

    def execute_query(self, query: str, *options) -> None:
        self.cur.execute(query, options)
        self.con.commit()


password_store = PasswordStore()
password_store.create_passwords_table()
password_store.create_token_table()
