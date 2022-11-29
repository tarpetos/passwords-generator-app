import sqlite3


class StoreUserPasswords:
    def __init__(self):
        self.con = sqlite3.connect('passwords\\your_passwords_database')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password_usage VARCHAR(384) NOT NULL,
                password VARCHAR(384) NOT NULL,
                password_length INTEGER NOT NULL,
                password_has_repeatable BOOL NOT NULL,
                CONSTRAINT unique_data UNIQUE(password_usage)
            )
            """
        )

    def insert_to_tb(self, password_usage, password, password_length, password_has_repeatable):
        self.cur.execute(
            "INSERT OR IGNORE INTO passwords(password_usage, password, password_length, password_has_repeatable) "
            "VALUES (?, ?, ?, ?)",
            (password_usage, password, password_length, password_has_repeatable)
        )

        self.con.commit()

    def select_descriptions(self) -> list:
        self.cur.execute(
            "SELECT password_usage FROM passwords "
            "ORDER BY id"
        )

        password_list = self.cur.fetchall()

        return password_list

    def update_existing_password(self, password, password_length, password_has_repeatable, password_usage):
        self.cur.execute(
            "UPDATE passwords "
            "SET password = ?, password_length = ?, password_has_repeatable = ? "
            "WHERE password_usage = ?",
            (password, password_length, password_has_repeatable, password_usage)
        )

        self.con.commit()
