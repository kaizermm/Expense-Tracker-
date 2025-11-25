import sqlite3
import json
import os

def load_config():
    #find the project folder
    project_folder=os.path.dirname(os.path.dirname(__file__))
    config_file_p=os.path.join(project_folder,"config","config.json")
    #open the file and read json
    with open(config_file_p,"r") as file:
        config_data=json.load(file)
    return config_data

def get_connection():
    config=load_config()
    #get database and filename
    database_name=config.get("database_path","expenses.db")
    # database is stored in the project folder
    project_folder = os.path.dirname(os.path.dirname(__file__))
    database_full_path = os.path.join(project_folder, database_name)
    # connect to the SQLite database (creates the file if it does not exist)
    connection = sqlite3.connect(database_full_path)
    return connection

def initialize_db():
    """Create the tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT);
        
    """)

    # create budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(month, year)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
    print("Database initialized.")



