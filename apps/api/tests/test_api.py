from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['data_status']=='DEMO'
def test_stock():
    r=client.get('/api/v1/stocks/RELIANCE'); assert r.status_code==200; assert r.json()['data_status']=='DEMO'
def test_scanner(): assert client.get('/api/v1/scanner').status_code==200

def test_market_session_holiday():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from app.services.market_session import market_session

    result = market_session(datetime(2026, 9, 14, 10, 0, tzinfo=ZoneInfo("Asia/Kolkata")))

    assert result["session"] == "CLOSED"
    assert result["is_open"] is False

def test_market_session_next_trading_session_skips_holiday():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from app.services.market_session import market_session

    result = market_session(datetime(2026, 9, 14, 16, 30, tzinfo=ZoneInfo("Asia/Kolkata")))

    assert result["next_session_open"] == "2026-09-15T09:15:00+05:30"

def test_provider_status():
    response = client.get("/api/v1/providers/status")
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mock"
    assert body["implemented"] is True
