from database import create_db
import sqlite3

sample_bugs = [
    ("Crash on login", "App crashes when entering wrong password", "High"),
    ("UI glitch", "Button overlaps on small screens", "Low"),
    ("Performance issue", "App slows down after 1 hour of usage", "Medium"),
    ("Data loss", "File not saved when power cuts", "Critical"),
    ("Security flaw", "Password visible in logs", "Critical"),
    ("Minor typo", "Spelling mistake in settings page", "Low"),
    ("Memory leak", "RAM usage increases continuously", "High")
]

def insert_samples():
    create_db()
    conn = sqlite3.connect("bugs.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO bugs (title, description, severity) VALUES (?, ?, ?)", sample_bugs)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_samples()
    print("Sample data inserted successfully.")
