from __future__ import annotations

from ..market_data import MarketDataProvider


SUPPORTED_PROVIDERS = {
    "mock": "Demo/mock market data",
    "demo": "Demo/mock market data",
    "http": "Generic HTTP market-data adapter",
    "dhan": "DhanHQ market-data adapter",
    "upstox": "Upstox V3 market-data adapter",
    "angelone": "Angel One SmartAPI market-data adapter",
}


def validate_provider_name(name: str) -> str:
    normalized = name.strip().lower()
    if normalized not in SUPPORTED_PROVIDERS:
        supported = ", ".join(SUPPORTED_PROVIDERS)
        raise ValueError(
            f"Unsupported MARKET_DATA_PROVIDER: {normalized}. "
            f"Supported providers: {supported}"
        )
    return normalized


def provider_status(name: str) -> dict:
    normalized = validate_provider_name(name)
    return {
        "provider": normalized,
        "description": SUPPORTED_PROVIDERS[normalized],
        "implemented": normalized in {"mock", "demo", "http"},
    }
