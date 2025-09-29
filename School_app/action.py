import sqlite3
connected = sqlite3.connect("School_app.db", check_same_thread=False)

# This script is  create tabel automatically when you run the flet app

def create_table():
    c = connected.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            contact TEXT,
            email TEXT,
            address TEXT
            gender TEXT)
             """)
    connected.commit()