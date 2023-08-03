from typing import Tuple, List, Any

from .local_db_connector import LocalDatabaseConnector


class PasswordStore(LocalDatabaseConnector):
    def __init__(self):
        super().__init__()
        self.create_passwords_table()
        self.create_history_table()

    def create_passwords_table(self):
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

    def history_insert(self, description: str, password: str):
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

    def history_update(self, description: str, password: str):
        self.cur.execute(
            '''
            UPDATE generation_history
            SET update_date = datetime('now', 'localtime')
            WHERE description = ? AND password = ?
            ''', (description, password)
        )
        self.con.commit()

    def history_delete(self, description: str, password: str):
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

    def history_clear(self):
        self.cur.execute('DELETE FROM generation_history')
        self.con.commit()

    def history_get_table_size(self) -> Tuple[int]:
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

    def insert_update_into_tb(self, description: str, password: str, length: int, has_repeatable: bool):
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

    def drop_table(self):
        select_all_desc_and_pass = self.select_descriptions_password()

        for value in select_all_desc_and_pass:
            self.history_delete(*value)

        self.cur.execute('DROP TABLE IF EXISTS passwords')
        self.con.commit()

    def update_password_data_by_id(
            self,
            description: str,
            password: str,
            length: int,
            has_repeatable: bool,
            table_id: int
    ):
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

    def update_existing_password(self, password: str, length: int, has_repeatable: bool, description: str):
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

    def update_password_by_description(self, description: str, password: str):
        self.cur.execute(
            '''
            UPDATE passwords
            SET password =  ?
            WHERE description =  ?
            ''',
            (password, description)
        )
        self.con.commit()

    def select_descriptions(self) -> List[Any]:
        self.cur.execute(
            '''
            SELECT description FROM passwords
            ORDER BY id
            '''
        )

        description_list = self.cur.fetchall()
        self.con.commit()

        return description_list

    def select_description_password_by_id(self, row_id: int) -> Tuple[int]:
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            WHERE id = ?
            ''', (row_id,)
        )

        description = self.cur.fetchone()
        self.con.commit()

        return description

    def select_descriptions_password(self) -> List[Any]:
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            ORDER BY id
            '''
        )

        password_main_data_list = self.cur.fetchall()
        self.con.commit()

        return password_main_data_list

    def select_id(self) -> List[Any]:
        self.cur.execute(
            '''
            SELECT id FROM passwords
            ORDER BY id
            '''
        )

        id_data_list = self.cur.fetchall()
        self.con.commit()

        return id_data_list

    def select_record_by_id(self, table_id: int) -> Tuple[str]:
        self.cur.execute(
            '''
            SELECT description, password FROM passwords
            WHERE id = ?
            ''', (table_id,)
        )
        get_values = self.cur.fetchone()
        self.con.commit()

        return get_values

    def select_password_by_description(self, description: str) -> Any:
        self.cur.execute(
            '''
            SELECT password FROM passwords
            WHERE description = ?
            ORDER BY id
            ''', (description,)
        )

        get_values = self.cur.fetchone()
        self.con.commit()

        return get_values

    def delete_by_id(self, table_id: int):
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

    def select_search_data_by_desc(self, search_query: str) -> List[Tuple[int | str]]:
        self.cur.execute(
            '''
            SELECT id, description, password FROM passwords
            WHERE LOWER(description) LIKE '%' || LOWER(?) || '%'
            ORDER BY id
            ''', (search_query,)
        )
        main_data_list = self.cur.fetchall()
        # print(main_data_list)

        # main_data_list = pd.read_sql_query(
        #     '''
        #     SELECT id, description, password FROM passwords
        #     WHERE LOWER(description) LIKE '%' || LOWER(?) || '%'
        #     ORDER BY id
        #     ''', self.con, params=[search_query, ]
        # )
        # # print(main_data_list)

        self.con.commit()

        return main_data_list

    def select_full_table(self) -> List[Tuple[int | str]]:
        # password_data_list = pd.read_sql_query('SELECT * FROM passwords', self.con)

        self.cur.execute('SELECT * FROM passwords')
        password_data_list = self.cur.fetchall()

        self.con.commit()

        return password_data_list

    def select_full_history_table(self) -> List[Tuple[int | str]]:
        # password_data_list = pd.read_sql_query('SELECT * FROM generation_history ORDER BY description', self.con)

        self.cur.execute('SELECT * FROM generation_history ORDER BY description')
        password_data_list = self.cur.fetchall()

        self.con.commit()

        return password_data_list
