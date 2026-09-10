from __future__ import annotations

import os
from typing import Any

import requests

from ...market_data import Candle, MarketDataProvider, Quote


class DhanMarketDataProvider(MarketDataProvider):
    """DhanHQ market-data adapter.

    This adapter is analysis-only. It does not place orders.
    """

    BASE_URL = "https://api.dhan.co/v2"

    def __init__(self) -> None:
        self.access_token = os.getenv("DHAN_ACCESS_TOKEN")
        self.client_id = os.getenv("DHAN_CLIENT_ID")

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
        raise NotImplementedError(
            "Dhan quote mapping requires the Dhan security ID for the symbol."
        )

    def get_historical_data(
        self,
        symbol: str,
        limit: int = 252,
    ) -> list[Candle]:
        raise NotImplementedError(
            "Dhan historical data requires the Dhan security ID mapping."
        )

    def get_intraday_candles(
        self,
        symbol: str,
        limit: int = 100,
    ) -> list[Candle]:
        raise NotImplementedError(
            "Dhan intraday data requires the Dhan security ID mapping."
        )

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
