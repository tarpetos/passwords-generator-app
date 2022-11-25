import sqlite3


class StoreUserPasswords:
    def __init__(self):
        self.con = sqlite3.connect('passwords/your_passwords_database')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password_usage VARCHAR(384) NOT NULL,
                password VARCHAR(384) NOT NULL,
                password_length INT NOT NULL,
                password_has_repeatable BOOL NOT NULL,
                CONSTRAINT unique_data UNIQUE(password_usage, password)
            )
            """
        )

    def insert_to_tb(self, password_usage, password, password_length, password_has_repeatable):
        self.cur.execute(
            "INSERT OR IGNORE INTO passwords (password_usage, password, password_length, password_has_repeatable) "
            "VALUES (?, ?, ?, ?)",
            (password_usage, password, password_length, password_has_repeatable)
        )

        self.con.commit()
