import aiosqlite
from bot_config import DB_NAME



async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            grade TEXT
        );

        CREATE TABLE IF NOT EXISTS points (
            user_id INTEGER PRIMARY KEY,
            points INTEGER,
            name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS polls (
            poll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT
        );

        CREATE TABLE IF NOT EXISTS poll_options (
            option_id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            option_text TEXT
        );

        CREATE TABLE IF NOT EXISTS poll_results (
            poll_id INTEGER,
            user_id INTEGER,
            option_id INTEGER,
            PRIMARY KEY (poll_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS poll_messages (
            poll_id INTEGER,
            user_id INTEGER,
            message_id INTEGER,
            PRIMARY KEY (poll_id, user_id)
        );
        """)
        await db.commit()
