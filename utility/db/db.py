import aiosqlite
from typing import Optional, Any

conn: Optional[aiosqlite.Connection] = None
db_type = "sqlite"
path = "data/bot_data.db"

class DatabaseClient:
    @staticmethod
    async def init():
        global conn
        
        if db_type == "sqlite":
            conn = await aiosqlite.connect(path)
            await conn.execute("PRAGMA foreign_keys = ON;")
            await conn.commit()

    @staticmethod
    async def close():
        if conn:
            await conn.close()

    @staticmethod
    async def execute(query: str, params: Optional[tuple] = None):
        if not conn:
            raise RuntimeError("Database not connected.")
        async with conn.execute(query, params or []) as cursor:
            await conn.commit()
            return cursor

    @staticmethod
    async def fetchone(query: str, params: Optional[tuple] = None) -> Optional[Any]:
        if not conn:
            raise RuntimeError("Database not connected.")
        async with conn.execute(query, params or []) as cursor:
            row = await cursor.fetchone()
            return row

    @staticmethod
    async def fetchall(query: str, params: Optional[tuple] = None):
        if not conn:
            raise RuntimeError("Database not connected.")
        async with conn.execute(query, params or []) as cursor:
            rows = await cursor.fetchall()
            return rows
