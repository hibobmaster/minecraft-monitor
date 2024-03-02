import sqlite3
class MCDB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS mcstatus (
                time TEXT NOT NULL,
                latency REAL NOT NULL
            )"""
        )
        self.conn.commit()

    def insert_time_and_latency(self, time, latency):
        self.cursor.execute("""
            INSERT INTO mcstatus (time, latency)
            VALUES (?, ?)
        """, (time, latency))
        self.conn.commit()