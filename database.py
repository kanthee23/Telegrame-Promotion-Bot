import sqlite3
import os

DB_PATH = "data/promos.db"

def connect():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS promos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            file_id TEXT,
            media_type TEXT
        )
    """)
    con.commit()
    con.close()

def save_promo(name, file_id, media_type):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO promos (name, file_id, media_type) VALUES (?, ?, ?)",
        (name, file_id, media_type)
    )
    con.commit()
    con.close()

def get_promo(name):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT file_id, media_type FROM promos WHERE name=?", (name,))
    row = cur.fetchone()
    con.close()
    return row

def list_promos():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT name FROM promos")
    rows = cur.fetchall()
    con.close()
    return [r[0] for r in rows]

