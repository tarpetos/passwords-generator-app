import os
import sqlite3
import pandas as pd

from typing import Iterator


def create_directory():
    if not os.path.exists('.passwords'):
        os.mkdir('.passwords')


class PasswordStore:
    def __init__(self):
        create_directory()
        self.con = sqlite3.connect('.passwords/data')
        self.cur = self.con.cursor()
        self.create_table()
        self.create_token_id_table()

    def create_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description VARCHAR(384) NOT NULL,
                password VARCHAR(384) NOT NULL,
                length INTEGER NOT NULL,
                has_repeatable BOOLEAN NOT NULL,
                CONSTRAINT unique_data UNIQUE(description)
            )
            '''
        )
        self.con.commit()

    def drop_table(self):
        self.cur.execute('DROP TABLE IF EXISTS passwords')
        self.con.commit()

    def create_token_id_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS id_token (
                saved_id INTEGER NOT NULL,
                saved_token VARCHAR(384) NOT NULL
            )
            '''
        )
        self.con.commit()

    def insert_into_tb(self, description, password, length, has_repeatable):
        self.cur.execute(
            '''
            INSERT OR IGNORE INTO passwords(description, password, length, has_repeatable)
            VALUES (?, ?, ?, ?)
            ''',
            (description, password, length, has_repeatable)
        )

        self.con.commit()

    def insert_update_into_tb(self, description, password, length, has_repeatable):
        self.cur.execute(
            '''
            REPLACE INTO passwords(description, password, length, has_repeatable)
            VALUES (?, ?, ?, ?)
            ''',
            (description, password, length, has_repeatable)
        )

        self.con.commit()

    def insert_into_save_tb(self, user_id, user_token):
        self.cur.execute(
            '''
            INSERT INTO id_token(saved_id, saved_token)
            VALUES (?, ?)
            ''',
            (user_id, user_token)
        )

        self.con.commit()

    def truncate_saved_token(self):
        self.cur.execute('DELETE FROM id_token')
        self.con.commit()

    def select_from_save_tb(self):
        self.cur.execute('SELECT * FROM id_token')

        result = self.cur.fetchall()

        self.con.commit()

        if result:
            return result[0]

    def update_password_data_by_id(self, description, password, length, has_repeatable, table_id):
        self.cur.execute(
            '''
            UPDATE passwords
            SET description =  ?, password =  ?, length =  ?, has_repeatable =  ?
            WHERE id =  ?
            ''',
            (description, password, length, has_repeatable, table_id)
        )

        self.con.commit()

    def update_existing_password(self, password, length, has_repeatable, description):
        self.cur.execute(
            '''
            UPDATE passwords
            SET password =  ?, length =  ?, has_repeatable =  ?
            WHERE description =  ?
            ''',
            (password, length, has_repeatable, description)
        )

        self.con.commit()

    def select_descriptions(self) -> list:
        self.cur.execute(
            '''
            SELECT description FROM passwords
            ORDER BY id
            '''
        )

        description_list = self.cur.fetchall()

        self.con.commit()

        return description_list

    def select_descriptions_password(self) -> list:
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            ORDER BY id
            '''
        )

        password_main_data_list = self.cur.fetchall()

        self.con.commit()

        return password_main_data_list

    def select_search_data_by_desc(self, search_query) -> tuple:
        self.cur.execute(
            '''
            SELECT id, description, password FROM passwords
            WHERE description = ?
            ORDER BY id
            ''', (search_query,)
        )

        main_data_list = self.cur.fetchone()

        self.con.commit()

        return main_data_list

    def select_full_table(self) -> Iterator[pd.DataFrame] | pd.DataFrame:
        password_data_list = pd.read_sql_query('SELECT * FROM passwords', self.con)

        self.con.commit()

        return password_data_list

    def select_id(self) -> list:
        self.cur.execute(
            '''
            SELECT id FROM passwords
            ORDER BY id
            '''
        )

        id_data_list = self.cur.fetchall()

        self.con.commit()

        return id_data_list

    def select_without_id(self) -> list:
        self.cur.execute(
            '''
            SELECT description, password, length, has_repeatable FROM passwords
            ORDER BY id
            '''
        )

        data_list = self.cur.fetchall()

        self.con.commit()

        return data_list

    def delete_by_id(self, table_id):
        self.cur.execute(
            '''
            DELETE FROM passwords
            WHERE id =  ?
            ''',
            (table_id,)
        )

        self.con.commit()
