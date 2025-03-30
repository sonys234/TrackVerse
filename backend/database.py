import sqlite3

conn = sqlite3.connect("tasks.db")  # Make sure this matches your Flask app's database file
cursor = conn.cursor()

# Create the 'tasks' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    due_date TEXT,
    task_time TEXT,
    priority TEXT,
    completed INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()

print("✅ Table 'tasks' created successfully!")
