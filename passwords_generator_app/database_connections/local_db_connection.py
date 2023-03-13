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
        self.create_history_table()

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

    def create_history_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS generation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description VARCHAR(384) NOT NULL,
                password VARCHAR(384) NOT NULL,
                add_date TEXT DEFAULT (datetime('now', 'localtime')) NOT NULL,
                update_date TEXT DEFAULT '-' NOT NULL,
                delete_date TEXT DEFAULT '-' NOT NULL,
                CONSTRAINT unique_data UNIQUE(description, password)
            )
            '''
        )
        self.con.commit()

    def history_insert(self, description, password):
        current_history_size = self.history_get_table_size()[0]

        if current_history_size >= 5000:
            self.history_remove_oldest_records()

        self.cur.execute(
            '''
            REPLACE INTO generation_history(description, password, add_date)
            VALUES (?, ?, datetime('now', 'localtime'));
            ''', (description, password)
        )
        self.con.commit()

    def history_update(self, description, password):
        self.cur.execute(
            '''
            UPDATE generation_history
            SET update_date = datetime('now', 'localtime')
            WHERE description = ? AND password = ?
            ''', (description, password)
        )
        self.con.commit()

    def history_delete(self, description, password):
        self.cur.execute(
            '''
            UPDATE generation_history
            SET delete_date = datetime('now', 'localtime')
            WHERE description = ? AND password = ?
            ''', (description, password)
        )
        self.con.commit()

    def history_remove_oldest_records(self):
        self.cur.execute(
            '''
            DELETE FROM generation_history 
            WHERE id IN (
                SELECT id 
                FROM generation_history 
                ORDER BY add_date 
                LIMIT 2500
            )
            '''
        )
        self.con.commit()

    def history_get_table_size(self) -> tuple:
        self.cur.execute('SELECT COUNT(id) FROM generation_history')

        table_size = self.cur.fetchone()
        self.con.commit()

        return table_size

    def insert_into_tb(self, description, password, length, has_repeatable):
        self.cur.execute(
            '''
            INSERT OR IGNORE INTO passwords(description, password, length, has_repeatable)
            VALUES (?, ?, ?, ?)
            ''',
            (description, password, length, has_repeatable)
        )

        self.con.commit()

        self.history_insert(description, password)

    def insert_update_into_tb(self, description, password, length, has_repeatable):
        self.cur.execute(
            '''
            SELECT description FROM passwords
            WHERE description = ?
            ''', (description,)
        )

        searched_description = self.cur.fetchone()
        self.con.commit()

        if searched_description:
            self.update_existing_password(password, length, has_repeatable, description)
        else:
            self.insert_into_tb(description, password, length, has_repeatable)

    def insert_into_save_tb(self, user_id, user_token):
        self.cur.execute(
            '''
            INSERT INTO id_token(saved_id, saved_token)
            VALUES (?, ?)
            ''',
            (user_id, user_token)
        )

        self.con.commit()

    def drop_table(self):
        select_all_desc_and_pass = self.select_descriptions_password()

        for value in select_all_desc_and_pass:
            self.history_delete(*value)

        self.cur.execute('DROP TABLE IF EXISTS passwords')
        self.con.commit()

    def truncate_saved_token(self):
        self.cur.execute('DELETE FROM id_token')
        self.con.commit()

    def select_from_save_tb(self) -> tuple[str, str] | None:
        self.cur.execute('SELECT * FROM id_token')

        result = self.cur.fetchone()
        self.con.commit()

        return result if result else None

    def update_password_data_by_id(self, description, password, length, has_repeatable, table_id):
        old_password = self.select_password_by_description(description)
        old_values_tuple = self.select_description_password_by_id(table_id)

        self.cur.execute(
            '''
            UPDATE passwords
            SET description =  ?, password =  ?, length =  ?, has_repeatable =  ?
            WHERE id =  ?
            ''',
            (description, password, length, has_repeatable, table_id)
        )
        self.con.commit()

        if old_password is None:
            self.history_update(*old_values_tuple)
            self.history_insert(description, password)
        else:
            self.history_update(description, *old_password)
            self.history_insert(description, password)

    def update_existing_password(self, password, length, has_repeatable, description):
        old_password = self.select_password_by_description(description)

        self.cur.execute(
            '''
            UPDATE passwords
            SET password =  ?, length =  ?, has_repeatable =  ?
            WHERE description =  ?
            ''',
            (password, length, has_repeatable, description)
        )
        self.con.commit()

        self.history_update(description, *old_password)
        self.history_insert(description, password)

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

    def select_description_by_id(self, row_id) -> tuple:
        self.cur.execute(
            '''
            SELECT description FROM passwords
            WHERE id = ?
            ''', (row_id, )
        )

        description = self.cur.fetchone()
        self.con.commit()

        return description

    def select_description_password_by_id(self, row_id) -> tuple:
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            WHERE id = ?
            ''', (row_id, )
        )

        description = self.cur.fetchone()
        self.con.commit()

        return description

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

    def select_search_data_by_desc(self, search_query: str) -> Iterator[pd.DataFrame] | pd.DataFrame:
        main_data_list = pd.read_sql_query(
            '''
            SELECT id, description, password FROM passwords
            WHERE LOWER(description) LIKE '%' || LOWER(?) || '%'
            ORDER BY id
            ''', self.con, params=[search_query, ]
        )

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

    def select_record_by_id(self, table_id):
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            WHERE id = ?
            ''', (table_id, )
        )
        get_values = self.cur.fetchone()
        self.con.commit()

        return get_values

    def select_password_by_description(self, description):
        self.cur.execute(
            '''
            SELECT password FROM passwords
            WHERE description = ?
            ORDER BY id
            ''', (description, )
        )

        get_values = self.cur.fetchone()
        self.con.commit()

        return get_values

    def delete_by_id(self, table_id):
        desc_and_pass = self.select_record_by_id(table_id)

        self.cur.execute(
            '''
            DELETE FROM passwords
            WHERE id =  ?
            ''',
            (table_id,)
        )
        self.con.commit()

        self.history_delete(desc_and_pass[0], desc_and_pass[1])
