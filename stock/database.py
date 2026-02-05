import sqlite3

def connect():
    return sqlite3.connect("trades.db", check_same_thread=False)

def create_table():
    conn = connect()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY,
        stock TEXT,
        buy_price REAL,
        stoploss REAL,
        target REAL,
        status TEXT
    )
    """)
    conn.commit()
