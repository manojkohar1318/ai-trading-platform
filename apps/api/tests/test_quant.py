from app.quant.indicators import sma,ema,rsi,vwap

def test_sma(): assert sma([1,2,3,4],3)==[None,None,2,3]
def test_ema_starts_at_sma(): assert ema([1,2,3],3)[2]==2
def test_rsi_uptrend(): assert rsi(list(range(1,20)),14)[-1]==100
def test_vwap(): assert vwap([2,3],[0,1],[1,2],[10,10])[-1]==1.5
