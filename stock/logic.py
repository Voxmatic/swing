from database import conn, c
from price_fetch import get_price

def update_trades():
    rows = c.execute("SELECT * FROM trades").fetchall()

    for r in rows:
        id, sym, buy, sl, tgt, status, triggered = r
        price = get_price(sym)

        if not triggered and price >= buy:
            c.execute("UPDATE trades SET entry_triggered=1, status='ACTIVE' WHERE id=?", (id,))

        elif triggered:
            if price >= tgt:
                c.execute("UPDATE trades SET status='TARGET HIT' WHERE id=?", (id,))
            elif price <= sl:
                c.execute("UPDATE trades SET status='STOPLOSS HIT' WHERE id=?", (id,))

    conn.commit()
