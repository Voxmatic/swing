import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1441848805086593198/G8qxJoQ6Rm8ChKGjJ24sucSruKAaNFd5FeDI-T-usEfAhfHPe5CqeRxZIIXRJZC6knFE"


def send_alert(symbol, direction):
    emoji = "🟢"

    payload = {
        "content": (
            f"{emoji} **NRT BULLISH SIGNAL** {emoji}\n\n"
            f"**Symbol:** {symbol}\n"
            f"**Condition:** PRICE + TIME + BIAS aligned\n"
            f"**Timeframe:** Daily (Filtered by Weekly)\n"
        )
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print("DISCORD ERROR:", e)
