#sqlite_storage.py

import sqlite3
from core.models import ProcessedText
from core.storage.base import TextStorageBase


class SQLiteTextStorage(TextStorageBase):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS texts (
                    content TEXT PRIMARY KEY,
                    timestamp REAL,
                    length INTEGER
                );
                """)
        self.conn.commit()
        cursor.close()

    def exists(self, content: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(""" SELECT 1 FROM texts WHERE content = ? LIMIT 1""", (content,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def save(self, processed: ProcessedText) -> None:
        if self.exists(processed.content):
            return
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO texts (content, timestamp, length) VALUES (?, ?, ?)""",
                       (processed.content, processed.timestamp, processed.length))
        self.conn.commit()
        cursor.close()


    def load_all(self) -> list[ProcessedText]:
        cursor = self.conn.cursor()
        cursor.execute(""" SELECT content, timestamp, length FROM texts""")
        rows = cursor.fetchall()
        cursor.close()

        return [ProcessedText(content=row[0], timestamp=row[1], length=row[2]) for row in rows]

    def close(self):
        self.conn.close()
