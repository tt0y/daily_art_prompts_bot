import aiosqlite
import os

class Storage:
    def __init__(self, db_file: str):
        self.db_file = db_file

    async def init_db(self):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def add_chat(self, chat_id: int):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("INSERT OR IGNORE INTO chats (chat_id) VALUES (?)", (chat_id,))
            await db.commit()

    async def remove_chat(self, chat_id: int):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
            await db.commit()

    async def get_all_chats(self):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT chat_id FROM chats") as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
