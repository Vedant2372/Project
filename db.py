import sqlite3
from Project.config import DB_PATH
import os

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create documents metadata table
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            path TEXT PRIMARY KEY,
            filename TEXT,
            filetype TEXT,
            modified TEXT
        )
    """)

    # Create full-text search virtual table (FTS5)
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
        USING fts5(path, content)
    """)

    conn.commit()
    conn.close()

def insert_metadata(docs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for doc in docs:
        filename = doc["filename"]
        path = doc["path"]
        filetype = os.path.splitext(filename)[1]
        modified = str(doc["modified"])
        content = doc["content"]

        c.execute("""
            INSERT OR REPLACE INTO documents (path, filename, filetype, modified)
            VALUES (?, ?, ?, ?)
        """, (path, filename, filetype, modified))

        c.execute("""
            INSERT OR REPLACE INTO documents_fts (path, content)
            VALUES (?, ?)
        """, (path, content))
    conn.commit()
    conn.close()

def get_all_metadata():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT path, filename, filetype, modified FROM documents")
    rows = c.fetchall()
    conn.close()
    return rows
