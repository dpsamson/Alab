import sqlite3

DB_PATH = "alab_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_memory(key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    return f"Saved: {key} = {value}"

def recall_memory(key: str = None):
    print("DEBUG recall_memory called with key:", key)
    conn = sqlite3.connect(DB_PATH)
    if key:
        cursor = conn.execute("SELECT value FROM memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]
    cursor = conn.execute("SELECT key, value FROM memory")
    rows = cursor.fetchall()
    conn.close()
    return {k: v for k, v in rows} if rows else "No memories found"

save_memory_schema = {
    "type": "function",
    "function": {
        "name": "save_memory",
        "description": "Save a piece of information to long-term memory, identified by a key",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "A short identifier for this memory, e.g. 'user_name' or 'favorite_course'"},
                "value": {"type": "string", "description": "The information to remember"}
            },
            "required": ["key", "value"]
        }
    }
}

recall_memory_schema = {
    "type": "function",
    "function": {
        "name": "recall_memory",
        "description": "Retrieve saved information. Provide a key if you know it, or omit it to retrieve all saved memories.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The identifier used when the memory was saved (optional)"}
            },
            "required": []
        }
    }
}