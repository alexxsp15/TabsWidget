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
            FOREIGN KEY (parent_folder_id) REFERENCES folder(id_folder) ON DELETE CASCADE
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

def get_root_folders():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM folder WHERE parent_folder_id IS NULL;")
    folders = cursor.fetchall()
    return folders

def add_folder(folder_name, parent_folder_id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO folder (folder_name, parent_folder_id) VALUES (?, ?)",
        (folder_name, parent_folder_id)
    )
    db.commit()
    db.close()

def get_other_folders():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM folder WHERE parent_folder_id IS NOT NULL;")
    folders = cursor.fetchall()
    return folders

def delete_folder(folder_id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT id_folder FROM folder WHERE parent_folder_id = ?", (folder_id,))
    child_folders = cursor.fetchall()

    for child in child_folders:
        delete_folder(child[0])

    cursor.execute("DELETE FROM folder WHERE id_folder = ?", (folder_id,))

    db.commit()
    db.close()

def add_tab(name, link, folder):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO tab (tab_name, tab_link, id_folder) VALUES (?, ?, ?)", (name, link, folder,))

    db.commit()
    db.close()

def get_all_tabs():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tab;")

    tabs = cursor.fetchall()
    return tabs

def get_tab_by_id(id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM tab WHERE id_tab = {id};")
    info = cursor.fetchall()

    return info

if __name__ == "__main__":
    init_db()
    print("Базу даних створено або оновлено ✅")