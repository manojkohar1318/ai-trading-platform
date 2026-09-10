from __future__ import annotations

from ..market_data import MarketDataProvider


class BrokerAdapterNotConfigured(MarketDataProvider):
    """Safe placeholder until a broker adapter is explicitly configured."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    def _raise(self) -> None:
        raise RuntimeError(
            f"{self.provider_name} market-data adapter is registered but "
            "not configured yet. Set up credentials and the official API "
            "adapter before enabling live data."
        )

    def get_quote(self, symbol: str):
        self._raise()

    def get_ohlc(self, symbol: str, limit: int = 100):
        self._raise()

    def get_intraday_candles(self, symbol: str, limit: int = 100):
        self._raise()

    def get_historical_data(self, symbol: str, limit: int = 252):
        self._raise()

    def get_index_data(self, symbol: str):
        self._raise()

    def get_market_breadth(self) -> dict:
        self._raise()
