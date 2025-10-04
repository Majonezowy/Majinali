from utility.db.db import DatabaseClient

async def setup_database(db: DatabaseClient):
    """Sets up the database and creates necessary tables."""
    await db.connect()
    
    await db.execute("""
    CREATE TABLE IF NOT EXISTS reaction_roles (
        guild_id INTEGER,
        channel_id INTEGER,
        message_id INTEGER,
        emoji TEXT,
        role_id INTEGER
    )
    """)
    
    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_reaction_roles_lookup
        ON reaction_roles (guild_id, message_id, emoji);
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS linked_text_channels (
            channel_id_a INTEGER NOT NULL,
            channel_id_b INTEGER NOT NULL,
            UNIQUE(channel_id_a, channel_id_b)
        )
    """)

    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_linked_text_channels_lookup
        ON linked_text_channels (channel_id_a, channel_id_b);
    """)

    return db
    