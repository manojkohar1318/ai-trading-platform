from dataclasses import dataclass

@dataclass(frozen=True)
class RiskInput:
    capital: float
    risk_percent: float
    entry: float
    stop: float
    max_position_percent: float = 100.0

def calculate_position_size(x: RiskInput) -> dict:
    if x.capital <= 0:
        raise ValueError("capital must be positive")
    if not 0 < x.risk_percent <= 10:
        raise ValueError("risk_percent must be between 0 and 10")
    if x.entry <= 0 or x.stop <= 0 or x.entry == x.stop:
        raise ValueError("entry and stop must be positive and different")
    risk_per_share = abs(x.entry - x.stop)
    risk_amount = x.capital * x.risk_percent / 100
    quantity = int(risk_amount // risk_per_share)
    position_value = quantity * x.entry
    cap_limit = x.capital * x.max_position_percent / 100
    if position_value > cap_limit:
        quantity = int(cap_limit // x.entry)
        position_value = quantity * x.entry
    return {
        "risk_amount": round(risk_amount, 2),
        "risk_per_share": round(risk_per_share, 4),
        "quantity": max(quantity, 0),
        "position_value": round(position_value, 2),
        "stop_distance_percent": round(risk_per_share / x.entry * 100, 4),
        "status": "ESTIMATE",
    }
