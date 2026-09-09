import pytest
from app.services.scoring import score_stock,ScoreWeights

def test_score_weighted(): assert score_stock({"trend":100,"momentum":100,"volume":100,"structure":100,"volatility":100,"risk_reward":100})["total_score"]==100
def test_weights_sum():
    with pytest.raises(ValueError): score_stock({"trend":100},ScoreWeights(.5,.5,0,0,0,.1))
