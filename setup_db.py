import sqlite3

def setup_database():
    """Sets up the database and creates necessary tables."""
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS reaction_roles (
        guild_id INTEGER,
        channel_id INTEGER,
        message_id INTEGER,
        emoji TEXT,
        role_id INTEGER
    )
    """)
    
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_reaction_roles_lookup
        ON reaction_roles (guild_id, message_id, emoji);
    """)
    
    conn.commit()
    conn.close()