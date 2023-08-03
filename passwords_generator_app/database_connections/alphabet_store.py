from typing import Tuple, Any

from ..database_connections.local_db_connector import LocalDatabaseConnector


class AlphabetStore(LocalDatabaseConnector):
    def __init__(self):
        super().__init__()
        self.create_alphabet_table()

    def create_alphabet_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS custom_alphabet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                letters VARCHAR(262),
                digits VARCHAR(262),
                punctuation VARCHAR(262)
            )
            '''
        )
        self.con.commit()

    def select_alphabet(self) -> Tuple[Any] | None:
        self.cur.execute(
            '''
            SELECT * FROM custom_alphabet
            '''
        )
        alphabet_data = self.cur.fetchone()
        self.con.commit()

        return alphabet_data

    def insert_into_alphabet(self, letters: str, digits: str, punctuation: str) -> None:
        self.cur.execute(
            '''
            INSERT INTO custom_alphabet(letters, digits, punctuation) 
            VALUES (?, ?, ?)
            ''', (letters, digits, punctuation)
        )
        self.con.commit()

    def update_alphabet(self, letters: str, digits: str, punctuation: str) -> None:
        self.cur.execute(
            '''
            UPDATE custom_alphabet
            SET letters = ?, digits = ?, punctuation = ?
            ''', (letters, digits, punctuation)
        )
        self.con.commit()
