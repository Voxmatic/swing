import sqlite3

DB_PATH = "nrt_states.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    SELECT symbol, date, price_state, time_state, close
    FROM states
    ORDER BY id DESC
""")

rows = cur.fetchall()

print("\n===================================================")
print("📊 NRT DATABASE VIEW")
print("===================================================\n")

for r in rows:
    print(f"SYMBOL : {r[0]}")
    print(f"DATE   : {r[1]}")
    print(f"PRICE  : {r[2]}")
    print(f"TIME   : {r[3]}")
    print(f"CLOSE  : {r[4]}")
    print("-" * 50)

conn.close()
