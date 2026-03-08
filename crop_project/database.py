import sqlite3

def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        disease TEXT,
        pest TEXT,
        confidence REAL,
        solution TEXT
    )
    """)

    conn.commit()
    conn.close()