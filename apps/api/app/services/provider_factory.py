from .market_data import MarketDataProvider, MockMarketDataProvider
from .http_market_data import HttpMarketDataProvider
from .providers.adapters import BrokerAdapterNotConfigured
from .providers.adapters.dhan import DhanMarketDataProvider
from .providers.registry import validate_provider_name
from ..core.config import get_settings


def build_market_data_provider() -> MarketDataProvider:
    settings = get_settings()
    name = validate_provider_name(settings.market_data_provider)

    if name in {"mock", "demo"}:
        return MockMarketDataProvider()

    if name == "http":
        return HttpMarketDataProvider(
            base_url=settings.market_api_base_url or "",
            api_key=settings.market_api_key,
        )

    # Broker adapters will be implemented one at a time against
    # their current official APIs. Never silently fall back to demo data.
    if name == "dhan":
        return DhanMarketDataProvider()

    if name in {"upstox", "angelone"}:
        return BrokerAdapterNotConfigured(name)

    raise ValueError(f"Unsupported MARKET_DATA_PROVIDER: {name}")
