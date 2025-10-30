import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tabs.db")

def connect_to_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS folder (
            id_folder INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT UNIQUE NOT NULL,
            parent_folder_id INTEGER,
            FOREIGN KEY (parent_folder_id) REFERENCES folder(id_folder) ON DELETE SET NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tab (
            id_tab INTEGER PRIMARY KEY AUTOINCREMENT,
            tab_name TEXT UNIQUE NOT NULL,
            tab_link TEXT UNIQUE NOT NULL,
            tab_description TEXT,
            tab_last_visited TEXT,
            tab_last_edited TEXT,
            tab_photo TEXT,
            id_folder INTEGER,
            FOREIGN KEY (id_folder) REFERENCES folder(id_folder) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Базу даних створено або оновлено ✅")