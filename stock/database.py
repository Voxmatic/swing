import sqlite3

conn = sqlite3.connect("trades.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS trades (
id INTEGER PRIMARY KEY,
symbol TEXT,
buy REAL,
sl REAL,
target REAL,
status TEXT,
entry_triggered INTEGER
)
""")

conn.commit()
