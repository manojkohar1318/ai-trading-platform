from dotenv import load_dotenv; load_dotenv()
from functools import lru_cache
import os

class Settings:
    environment: str = os.getenv("ENVIRONMENT", "development")
    market_data_provider: str = os.getenv("MARKET_DATA_PROVIDER", "mock")
    market_api_key: str | None = os.getenv("MARKET_API_KEY")
    market_api_base_url: str | None = os.getenv("MARKET_API_BASE_URL")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_service_role_key: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")

    @property
    def is_live_data(self) -> bool:
        return self.market_data_provider.lower() not in {"mock", "demo"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
