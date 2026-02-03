import sqlite3

DB_PATH = "nrt.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Delete Yahoo-style symbols (.NS)
cur.execute("""
    DELETE FROM nrt_states
    WHERE symbol LIKE '%.NS'
""")

conn.commit()
conn.close()

print("✅ Database cleanup completed: removed *.NS symbols")
