from .market_data import MarketDataProvider, MockMarketDataProvider
from .http_market_data import HttpMarketDataProvider
from ..core.config import get_settings

def build_market_data_provider() -> MarketDataProvider:
    settings = get_settings()
    name = settings.market_data_provider.lower()
    if name in {"mock", "demo"}:
        return MockMarketDataProvider()
    if name == "http":
        return HttpMarketDataProvider(
            base_url=settings.market_api_base_url or "",
            api_key=settings.market_api_key,
        )
    raise ValueError(f"Unsupported MARKET_DATA_PROVIDER: {name}")
