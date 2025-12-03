import sqlite3
import json
import os

def get_db_path():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    config_path = os.path.abspath(config_path)

    with open(config_path, "r") as f:
        config = json.load(f)

    return config["database_path"]

def get_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            amount REAL NOT NULL,
            PRIMARY KEY (month, year)
        )
    """)

    conn.commit()
    conn.close()




