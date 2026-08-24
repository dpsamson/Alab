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

def recall_memory(key: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT value FROM memory WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return f"No memory found for '{key}'"

save_memory_schema = {
    "type" : "function",
    "function": {
        "name": "save_memory",
        "description": "Save a piece of information to long-term memory, identified by a key",
        "parameters":{
            "type":"object",
            "properties":{
                "key": {"type":"string", "description": "A short identifier for this memory, e.g. 'user_name' or 'favorite_course'"},
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
        "description": "Retrieve a previously saved piece of information by its key",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The identifier used when the memory was saved"}
                },
                "required": ["key"]
            }
        }
    }