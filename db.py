import sqlite3
from datetime import datetime, timedelta

DB = "nrt_states.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS states(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        date TEXT,
        price_state TEXT,
        time_state TEXT,
        bias_state TEXT,
        close REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        symbol TEXT PRIMARY KEY,
        last_state TEXT,
        alert_time TEXT
    )
    """)

    con.commit()
    con.close()


def insert_state(
    *,
    symbol,
    price_state,
    time_state,
    bias_state,
    close
):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO states
    (symbol, date, price_state, time_state, bias_state, close)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        price_state,
        time_state,
        bias_state,
        close
    ))

    con.commit()
    con.close()


def last_alert(symbol):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT last_state, alert_time FROM alerts WHERE symbol=?",
        (symbol,)
    )
    r = cur.fetchone()
    con.close()
    return r


def update_alert(symbol, state):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO alerts
    (symbol, last_state, alert_time)
    VALUES (?, ?, ?)
    """, (
        symbol,
        state,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    con.commit()
    con.close()


def reset_alert(symbol):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM alerts WHERE symbol=?", (symbol,))
    con.commit()
    con.close()


def cooldown_ok(ts, hours=24):
    return (
        datetime.now() -
        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    ) >= timedelta(hours=hours)
