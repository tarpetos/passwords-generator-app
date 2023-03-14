import os

import mysql
import mysql.connector

from dotenv import load_dotenv, find_dotenv
from passwords_generator_app.user_actions_processing.encryption_decryption import decrypt


class RemoteDB:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.con = mysql.connector.connect(
            host=os.getenv('REMOTE_IP'),
            user=os.getenv('REMOTE_USER'),
            passwd=os.getenv('REMOTE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            connect_timeout=10,
        )

        self.cur = self.con.cursor()

    def select_all_tokens(self) -> list[str]:
        self.cur.execute(
            '''
            SELECT user_token FROM generated_tokens
            '''
        )

        all_tokens_tuple_lst = self.cur.fetchall()
        all_tokens_lst = [decrypt(token_tuple[0]) for token_tuple in all_tokens_tuple_lst]

        self.con.commit()

        return all_tokens_lst

    def select_id_by_token(self, entered_token: str) -> str | None:
        self.cur.execute(
            '''
            SELECT user_id FROM generated_tokens
            WHERE user_token = %s
            ''',
            (entered_token,)
        )

        get_id = self.cur.fetchone()

        self.con.commit()

        return get_id[0] if get_id else None

    def select_pass_gen_table_without_id(self, user_table_name: str) -> list[tuple, ...]:
        self.cur.execute(
            '''
            SELECT password_description, generated_password, password_length, has_repetetive FROM `%s`
            ORDER BY id;
            ''', (user_table_name,)
        )

        table_rows = self.cur.fetchall()

        self.con.commit()

        return table_rows

    def insert_update_password_data(
            self,
            user_id: str,
            user_desc: str,
            generated_pass: str,
            password_length: int,
            has_repetitive: bool
    ):
        self.cur.execute(
            f'''
            INSERT INTO `%s` (password_description, generated_password, password_length, has_repetetive) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE generated_password  = %s, password_length = %s, has_repetetive = %s
            ''',
            (user_id, user_desc, generated_pass, password_length,
             has_repetitive, generated_pass, password_length, has_repetitive)
        )

        self.con.commit()