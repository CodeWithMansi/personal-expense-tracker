import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS expense_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                item_price FLOAT,
                purchase_date DATE
            )"""
        )
        self.conn.commit()

    def fetch_records(self):
        self.cur.execute("SELECT * FROM expense_record")
        return self.cur.fetchall()

    def insert_record(self, item_name, item_price, purchase_date):
        self.cur.execute(
            "INSERT INTO expense_record (item_name, item_price, purchase_date) VALUES (?, ?, ?)",
            (item_name, item_price, purchase_date),
        )
        self.conn.commit()

    def remove_record(self, record_id):
        self.cur.execute("DELETE FROM expense_record WHERE id=?", (record_id,))
        self.conn.commit()

    def update_record(self, record_id, item_name, item_price, purchase_date):
        self.cur.execute(
            "UPDATE expense_record SET item_name=?, item_price=?, purchase_date=? WHERE id=?",
            (item_name, item_price, purchase_date, record_id),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
