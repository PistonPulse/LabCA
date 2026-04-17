import sqlite3

DB_FILE = "securenotes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Create notes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password_hash):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Parameterized query prevents SQL injection
    c.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Parameterized query prevents SQL injection
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    
    conn.close()
    return row

def create_note(user_id, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Parameterized query prevents SQL injection
    c.execute(
        "INSERT INTO notes (user_id, content) VALUES (?, ?)",
        (user_id, content)
    )
    
    conn.commit()
    conn.close()

def get_notes_by_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Parameterized query prevents SQL injection
    c.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = c.fetchall()
    
    conn.close()
    return rows
