import aiosqlite
import datetime
from .config import settings
import asyncio

_init_lock = asyncio.Lock()
_initialized = False

async def init_db():
    global _initialized
    async with _init_lock:
        if _initialized:
            return
        async with aiosqlite.connect(settings.sqlite_path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS weather_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
            """)
            await db.commit()
        _initialized = True

async def log_event(city: str, timestamp: str, file_path: str):
    await init_db()
    async with aiosqlite.connect(settings.sqlite_path) as db:
        await db.execute(
            "INSERT INTO weather_logs (city, timestamp, file_path) VALUES (?, ?, ?)",
            (city, timestamp, file_path)
        )
        await db.commit()