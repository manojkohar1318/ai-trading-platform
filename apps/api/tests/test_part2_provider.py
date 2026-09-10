import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

from app.services.market_data import MockMarketDataProvider
from app.services.risk import RiskInput, calculate_position_size

def test_mock_provider_is_demo():
    q = MockMarketDataProvider().get_quote("RELIANCE")
    assert q.is_demo is True
    assert q.price > 0

def test_risk_position_size():
    out = calculate_position_size(RiskInput(100000, 1, 1000, 980))
    assert out["risk_amount"] == 1000
    assert out["quantity"] == 50
    assert out["status"] == "ESTIMATE"
