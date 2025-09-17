import sqlite3
from datetime import datetime

DB_NAME = "bugs.db"

sample_bugs = [
    {"title": "Login button not working", "description": "Clicking login does nothing", "severity": "High", "priority": "High", "status": "Open", "assignee": "Alice"},
    {"title": "Page crashes on upload", "description": "Uploading large files causes server error", "severity": "Critical", "priority": "Critical", "status": "Open", "assignee": "Bob"},
    {"title": "Typo in homepage", "description": "Misspelled word 'Welcom' instead of 'Welcome'", "severity": "Low", "priority": "Low", "status": "Resolved", "assignee": "Charlie"},
    {"title": "Search bar slow response", "description": "Search results take too long to load", "severity": "Medium", "priority": "Medium", "status": "In Progress", "assignee": "Alice"},
    {"title": "Profile picture not updating", "description": "Uploading a new profile picture does not reflect", "severity": "High", "priority": "High", "status": "Open", "assignee": "David"},
    {"title": "Notifications not showing", "description": "Users don’t get new notifications", "severity": "Medium", "priority": "Medium", "status": "In Progress", "assignee": "Eve"},
    {"title": "Broken link in footer", "description": "Privacy policy link returns 404", "severity": "Low", "priority": "Low", "status": "Closed", "assignee": "Frank"},
    {"title": "Payment gateway error", "description": "Transaction fails for some credit cards", "severity": "Critical", "priority": "Critical", "status": "Resolved", "assignee": "Bob"},
    {"title": "Settings not saving", "description": "Changes in user settings are not persisted", "severity": "High", "priority": "High", "status": "In Progress", "assignee": "Charlie"},
    {"title": "Dark mode theme glitch", "description": "Some text not visible in dark mode", "severity": "Medium", "priority": "Medium", "status": "Open", "assignee": "Alice"}
]

# Connect to DB
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for bug in sample_bugs:
    cursor.execute("""
        INSERT INTO bugs (title, description, severity, priority, status, assignee, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bug["title"], bug["description"], bug["severity"], bug["priority"],
        bug["status"], bug["assignee"], datetime.now(), datetime.now()
    ))

conn.commit()
conn.close()
print("10 sample bugs added successfully!")

