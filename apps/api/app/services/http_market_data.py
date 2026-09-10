from datetime import datetime
import requests
from .market_data import MarketDataProvider, Quote, Candle

class HttpMarketDataProvider(MarketDataProvider):
    """Vendor-neutral HTTP adapter.

    The API contract is intentionally generic. Configure a gateway/vendor that
    exposes quote and candle endpoints rather than hard-coding broker URLs.
    """

    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _get(self, path: str, params: dict | None = None) -> dict:
        if not self.base_url:
            raise RuntimeError("Market data provider is not configured")
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.get(
            f"{self.base_url}/{path.lstrip('/')}",
            params=params or {},
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_quote(self, symbol: str) -> Quote:
        d = self._get(f"quote/{symbol.upper()}")
        return Quote(
            symbol=symbol.upper(),
            price=float(d["price"]),
            open=float(d["open"]),
            high=float(d["high"]),
            low=float(d["low"]),
            prev_close=float(d["previous_close"]),
            volume=int(d.get("volume", 0)),
            change_pct=float(d.get("change_percent", 0)),
            is_demo=False,
        )

    def _candles(self, symbol: str, path: str, limit: int) -> list[Candle]:
        rows = self._get(path, {"symbol": symbol.upper(), "limit": limit}).get("candles", [])
        return [
            Candle(
                timestamp=str(x["timestamp"]),
                open=float(x["open"]),
                high=float(x["high"]),
                low=float(x["low"]),
                close=float(x["close"]),
                volume=int(x.get("volume", 0)),
            )
            for x in rows
        ]

    def get_ohlc(self, symbol: str, limit: int = 100) -> list[Candle]:
        return self._candles(symbol, "candles", limit)

    def get_intraday_candles(self, symbol: str, limit: int = 100) -> list[Candle]:
        return self._candles(symbol, "candles/intraday", limit)

    def get_historical_data(self, symbol: str, limit: int = 252) -> list[Candle]:
        return self._candles(symbol, "candles/historical", limit)

    def get_index_data(self, symbol: str) -> Quote:
        return self.get_quote(symbol)

    def get_market_breadth(self) -> dict:
        return self._get("market/breadth")
