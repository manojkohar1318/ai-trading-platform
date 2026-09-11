import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

from app.services.market_data import MockMarketDataProvider
from app.services.risk import RiskInput, calculate_position_size

def test_mock_provider_is_demo():
    q = MockMarketDataProvider().get_quote("RELIANCE")
    assert q.is_demo is True
    assert q.price > 0

def test_risk_position_size():
    out = calculate_position_size(RiskInput(100000, 1, 1000, 980))
    assert out["risk_amount"] == 1000
    assert out["quantity"] == 50
    assert out["status"] == "ESTIMATE"

import pytest
from app.services.providers.adapters.dhan import DhanMarketDataProvider


def test_dhan_quote_calculates_change_pct():
    provider = object.__new__(DhanMarketDataProvider)
    provider.instrument_resolver = type(
        "Resolver",
        (),
        {"resolve": lambda self, symbol: "2885"},
    )()
    provider._post = lambda path, payload: {
        "data": {
            "NSE_EQ": {
                "2885": {
                    "last_price": 1020.0,
                    "ohlc": {
                        "open": 1010.0,
                        "high": 1030.0,
                        "low": 1005.0,
                        "close": 1000.0,
                    },
                    "volume": 500000,
                }
            }
        }
    }

    quote = provider.get_quote("RELIANCE")

    assert quote.change_pct == pytest.approx(2.0)
    assert quote.price == 1020.0
    assert quote.prev_close == 1000.0
    assert quote.is_demo is False

def test_dhan_quote_change_pct(monkeypatch):
    from app.services.providers.adapters.dhan import DhanMarketDataProvider

    provider = object.__new__(DhanMarketDataProvider)
    provider.instrument_resolver = type(
        "Resolver", (), {"resolve": lambda self, symbol: "2885"}
    )()
    provider._post = lambda path, payload: {
        "data": {
            "NSE_EQ": {
                "2885": {
                    "last_price": 2500.0,
                    "ohlc": {
                        "open": 2480.0,
                        "high": 2520.0,
                        "low": 2470.0,
                        "close": 2450.0,
                    },
                    "volume": 123456,
                }
            }
        }
    }

    quote = provider.get_quote("RELIANCE")

    assert quote.price == 2500.0
    assert quote.prev_close == 2450.0
    assert quote.volume == 123456
    assert abs(quote.change_pct - 2.0408163265306123) < 1e-9
    assert quote.is_demo is False

def test_dhan_intraday_uses_datetime_range():
    from app.services.providers.adapters.dhan import DhanMarketDataProvider

    provider = object.__new__(DhanMarketDataProvider)
    provider.instrument_resolver = type(
        "Resolver", (), {"resolve": lambda self, symbol: "2885"}
    )()

    captured = {}

    def fake_post(path, payload):
        captured["path"] = path
        captured["payload"] = payload
        return {
            "data": {
                "timestamp": [1757500200],
                "open": [2500.0],
                "high": [2505.0],
                "low": [2498.0],
                "close": [2503.0],
                "volume": [100000],
            }
        }

    provider._post = fake_post

    candles = provider.get_intraday_candles("RELIANCE", limit=1)

    assert captured["path"] == "/charts/intraday"
    assert captured["payload"]["securityId"] == "2885"
    assert captured["payload"]["exchangeSegment"] == "NSE_EQ"
    assert captured["payload"]["instrument"] == "EQUITY"
    assert captured["payload"]["interval"] == 1
    assert captured["payload"]["oi"] is False
    assert len(captured["payload"]["fromDate"]) == 19
    assert captured["payload"]["fromDate"].endswith("09:15:00")
    assert len(captured["payload"]["toDate"]) == 19
    assert " " in captured["payload"]["toDate"]
    assert len(candles) == 1
