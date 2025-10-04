import aiosqlite
from typing import Optional, Any

class DatabaseClient:
    def __init__(self) -> None:
        self.db_type = "sqlite"
        self.path = "data/bot_data.db"
        self.conn: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        if self.db_type == "sqlite":
            self.conn = await aiosqlite.connect(self.path)
            await self.conn.execute("PRAGMA foreign_keys = ON;")
            await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def execute(self, query: str, params: Optional[tuple] = None):
        if not self.conn:
            raise RuntimeError("Database not connected.")
        async with self.conn.execute(query, params or []) as cursor:
            await self.conn.commit()
            return cursor

    async def fetchone(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        if not self.conn:
            raise RuntimeError("Database not connected.")
        async with self.conn.execute(query, params or []) as cursor:
            row = await cursor.fetchone()
            return row

    async def fetchall(self, query: str, params: Optional[tuple] = None):
        if not self.conn:
            raise RuntimeError("Database not connected.")
        async with self.conn.execute(query, params or []) as cursor:
            rows = await cursor.fetchall()
            return rows
