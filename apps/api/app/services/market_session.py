from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

PRE_OPEN_START = time(9, 0)
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)
POST_CLOSE = time(16, 0)


def market_session(now: datetime | None = None) -> dict:
    now = (now or datetime.now(IST)).astimezone(IST)

    if now.weekday() >= 5:
        session = "CLOSED"
        is_open = False
    elif now.time() < PRE_OPEN_START:
        session = "CLOSED"
        is_open = False
    elif now.time() < MARKET_OPEN:
        session = "PRE_OPEN"
        is_open = False
    elif now.time() < MARKET_CLOSE:
        session = "OPEN"
        is_open = True
    elif now.time() < POST_CLOSE:
        session = "POST_MARKET"
        is_open = False
    else:
        session = "CLOSED"
        is_open = False

    return {
        "timezone": "Asia/Kolkata",
        "session": session,
        "is_open": is_open,
        "timestamp": now.isoformat(),
        "market_open": "09:15",
        "market_close": "15:30",
    }
