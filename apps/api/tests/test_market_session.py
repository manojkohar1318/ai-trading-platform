from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.market_session import market_session

IST = ZoneInfo("Asia/Kolkata")


def test_market_open():
    result = market_session(datetime(2026, 9, 11, 10, 0, tzinfo=IST))
    assert result["session"] == "OPEN"
    assert result["is_open"] is True


def test_pre_open():
    result = market_session(datetime(2026, 9, 11, 9, 5, tzinfo=IST))
    assert result["session"] == "PRE_OPEN"
    assert result["is_open"] is False


def test_after_market():
    result = market_session(datetime(2026, 9, 11, 16, 30, tzinfo=IST))
    assert result["session"] == "CLOSED"
    assert result["is_open"] is False


def test_weekend():
    result = market_session(datetime(2026, 9, 12, 10, 0, tzinfo=IST))
    assert result["session"] == "CLOSED"
    assert result["is_open"] is False
