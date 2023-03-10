import os
import mysql
import mysql.connector

from additional_modules.encryption_decryption import decrypt
from dotenv import load_dotenv, find_dotenv

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


    def select_all_tokens(self):
        self.cur.execute(
            '''
            SELECT user_token FROM generated_tokens
            '''
        )

        all_tokens_tuple_lst = self.cur.fetchall()
        all_tokens_lst = [decrypt(token_tuple[0]) for token_tuple in all_tokens_tuple_lst]

        self.con.commit()

        return all_tokens_lst


    def select_id_by_token(self, entered_token):
        self.cur.execute(
            '''
            SELECT user_id FROM generated_tokens
            WHERE user_token = %s
            ''',
            (entered_token,)
        )

        get_id = self.cur.fetchone()

        self.con.commit()

        if get_id:
            return get_id[0]


    def select_pass_gen_table_without_id(self, user_table_name):
        self.cur.execute(
            '''
            SELECT password_description, generated_password, password_length, has_repetetive FROM `%s`
            ORDER BY id;
            ''', (user_table_name,)
        )

        table_rows = self.cur.fetchall()

        self.con.commit()

        return table_rows


    def insert_update_password_data(self, user_id, user_desc, generated_pass, password_length, has_repetetive):
        self.cur.execute(
            '''
            INSERT INTO `%s` (password_description, generated_password, password_length, has_repetetive) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE generated_password  = %s, password_length = %s, has_repetetive = %s
            ''',
            (user_id, user_desc, generated_pass, password_length, has_repetetive,
             generated_pass, password_length, has_repetetive)
        )

        self.con.commit()
