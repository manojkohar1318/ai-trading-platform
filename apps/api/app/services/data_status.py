from dataclasses import dataclass
from enum import Enum

class DataStatus(str, Enum):
    LIVE = "LIVE"
    DELAYED = "DELAYED"
    DEMO = "DEMO"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"

@dataclass(frozen=True)
class DataQuality:
    status: DataStatus
    source: str
    as_of: str | None = None
    message: str | None = None
