from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

import requests

from ...market_data import Candle, MarketDataProvider, Quote
from ..instrument_resolver import DhanInstrumentResolver


class DhanMarketDataProvider(MarketDataProvider):
    """DhanHQ market-data adapter.

    This adapter is analysis-only. It does not place orders.
    """

    BASE_URL = "https://api.dhan.co/v2"

    def __init__(self) -> None:
        self.access_token = os.getenv("DHAN_ACCESS_TOKEN")
        self.client_id = os.getenv("DHAN_CLIENT_ID")
        self.instrument_resolver = DhanInstrumentResolver(
            os.getenv("DHAN_INSTRUMENT_MASTER_PATH", "data/dhan-instruments.csv")
        )

        if not self.access_token:
            raise ValueError("DHAN_ACCESS_TOKEN is required")
        if not self.client_id:
            raise ValueError("DHAN_CLIENT_ID is required")

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "access-token": self.access_token,
            "client-id": self.client_id,
        }

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            f"{self.BASE_URL}{path}",
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_quote(self, symbol: str) -> Quote:
        security_id = self.instrument_resolver.resolve(symbol)
        payload = {
            "NSE_EQ": [int(security_id)],
        }
        data = self._post("/marketfeed/quote", payload)
        row = data.get("data", {}).get("NSE_EQ", {}).get(str(security_id), {})
        if not row:
            raise ValueError(f"Dhan returned no quote for {symbol} ({security_id})")

        ohlc = row.get("ohlc", {})
        return Quote(
            symbol=symbol.upper(),
            price=float(row["last_price"]),
            open=float(ohlc.get("open", row.get("open", 0.0))),
            high=float(ohlc.get("high", row.get("high", 0.0))),
            low=float(ohlc.get("low", row.get("low", 0.0))),
            prev_close=float(ohlc.get("close", row.get("prev_close", 0.0))),
            volume=int(row.get("volume", 0)),
            change_pct=((float(row["last_price"]) - float(ohlc.get("close", row.get("prev_close", 0.0)))) / float(ohlc.get("close", row.get("prev_close", 0.0))) * 100.0) if float(ohlc.get("close", row.get("prev_close", 0.0))) else 0.0,
            is_demo=False,
        )

    def get_historical_data(
        self,
        symbol: str,
        limit: int = 252,
    ) -> list[Candle]:
        security_id = self.instrument_resolver.resolve(symbol)
        to_date = datetime.now().date()
        from_date = to_date - timedelta(days=max(limit * 2, 30))
        payload = {
            "securityId": security_id,
            "exchangeSegment": "NSE_EQ",
            "instrument": "EQUITY",
            "expiryCode": 0,
            "oi": False,
            "fromDate": from_date.isoformat(),
            "toDate": to_date.isoformat(),
        }
        data = self._post("/charts/historical", payload)
        return self._parse_candles(data, limit)

    def get_intraday_candles(
        self,
        symbol: str,
        limit: int = 100,
    ) -> list[Candle]:
        security_id = self.instrument_resolver.resolve(symbol)
        now = datetime.now()
        from_date = now.replace(hour=9, minute=15, second=0, microsecond=0)
        to_date = now
        payload = {
            "securityId": security_id,
            "exchangeSegment": "NSE_EQ",
            "instrument": "EQUITY",
            "interval": 1,
            "oi": False,
            "fromDate": from_date.isoformat(),
            "toDate": to_date.isoformat(),
        }
        data = self._post("/charts/intraday", payload)
        return self._parse_candles(data, limit)

    @staticmethod
    def _parse_candles(data: dict[str, Any], limit: int) -> list[Candle]:
        rows = data.get("data", data)
        if not isinstance(rows, dict):
            raise ValueError("Unexpected Dhan candle response")

        timestamps = rows.get("timestamp", [])
        opens = rows.get("open", [])
        highs = rows.get("high", [])
        lows = rows.get("low", [])
        closes = rows.get("close", [])
        volumes = rows.get("volume", [])

        size = min(len(timestamps), len(opens), len(highs), len(lows), len(closes), len(volumes))
        candles: list[Candle] = []

        for i in range(size):
            ts = timestamps[i]
            if isinstance(ts, (int, float)):
                timestamp = datetime.fromtimestamp(ts).isoformat()
            else:
                timestamp = str(ts)

            candles.append(
                Candle(
                    timestamp=timestamp,
                    open=float(opens[i]),
                    high=float(highs[i]),
                    low=float(lows[i]),
                    close=float(closes[i]),
                    volume=int(volumes[i]),
                )
            )

        return candles[-limit:]

    def get_ohlc(self, symbol: str, limit: int = 100) -> list[Candle]:
        return self.get_intraday_candles(symbol, limit)

    def get_index_data(self, symbol: str) -> Quote:
        return self.get_quote(symbol)

    def get_market_breadth(self) -> dict[str, Any]:
        return {
            "status": "UNAVAILABLE",
            "is_demo": False,
            "message": "Dhan market-breadth mapping is not configured yet.",
        }
