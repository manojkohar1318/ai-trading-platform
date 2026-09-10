from __future__ import annotations

import csv
from pathlib import Path


class DhanInstrumentResolver:
    """Resolve NSE equity trading symbols to Dhan Security IDs."""

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)
        self._cache: dict[str, str] | None = None

    def _load(self) -> dict[str, str]:
        if self._cache is not None:
            return self._cache

        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dhan instrument master not found: {self.csv_path}"
            )

        mapping: dict[str, str] = {}

        with self.csv_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if (
                    row.get("SEM_EXM_EXCH_ID") == "NSE"
                    and row.get("SEM_SEGMENT") == "E"
                    and row.get("SEM_INSTRUMENT_NAME") == "EQUITY"
                ):
                    symbol = (row.get("SEM_TRADING_SYMBOL") or "").strip().upper()
                    security_id = (row.get("SEM_SMST_SECURITY_ID") or "").strip()

                    if symbol and security_id:
                        mapping[symbol] = security_id

        self._cache = mapping
        return mapping

    def resolve(self, symbol: str) -> str:
        normalized = symbol.strip().upper()
        security_id = self._load().get(normalized)

        if not security_id:
            raise KeyError(
                f"Dhan Security ID not found for NSE equity symbol: {normalized}"
            )

        return security_id
