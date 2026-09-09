from .market_data import MarketDataProvider
from .scoring import score_stock
from .trade_setup import build_trade_setup
from ..quant.indicators import sma,ema,rsi,macd,atr,historical_volatility,vwap,relative_volume,volume_breakout,ema_crossover
from ..quant.structure import support_resistance,price_structure,breakout_breakdown

def analyze(provider:MarketDataProvider,symbol:str):
    candles=provider.get_historical_data(symbol,100); q=provider.get_quote(symbol)
    close=[c.close for c in candles]; high=[c.high for c in candles]; low=[c.low for c in candles]; vol=[c.volume for c in candles]
    sma20=sma(close,20)[-1]; ema9=ema(close,9)[-1]; ema21=ema(close,21)[-1]; r=rsi(close,14)[-1]; ml,ms,mh=macd(close); a=atr(high,low,close,14)[-1]; hv=historical_volatility(close,20)[-1]; vw=vwap(high,low,close,vol)[-1]; rv=relative_volume(vol,20)[-1]; vb=volume_breakout(vol,20)[-1]
    support,resistance=support_resistance(close); structure=price_structure(close); bb=breakout_breakdown(close)
    trend="bullish" if ema9 and ema21 and ema9>ema21 and q.price>(sma20 or q.price) else "bearish" if ema9 and ema21 and ema9<ema21 else "neutral"
    momentum=80 if (r or 50)>55 and (ml[-1] or 0)>0 else 55 if (r or 50)>45 else 35
    trend_score=85 if trend=="bullish" else 35 if trend=="bearish" else 55
    volume_score=85 if vb or (rv or 0)>1.5 else 65 if (rv or 0)>1 else 45
    structure_score=85 if structure["higher_highs"] and structure["higher_lows"] else 35 if structure["lower_highs"] and structure["lower_lows"] else 55
    volatility_score=70 if hv and hv<35 else 50
    rr=2.0 if a else 0
    risk_score=80 if rr>=1.8 else 55
    score=score_stock({"trend":trend_score,"momentum":momentum,"volume":volume_score,"structure":structure_score,"volatility":volatility_score,"risk_reward":risk_score})
    setup=build_trade_setup(q.price,support,resistance,a,score["total_score"],trend)
    return {"quote":q.__dict__,"indicators":{"sma20":sma20,"ema9":ema9,"ema21":ema21,"rsi":r,"macd":ml[-1],"macd_signal":ms[-1],"macd_histogram":mh[-1],"atr":a,"historical_volatility":hv,"vwap":vw,"relative_volume":rv},"structure":{**structure,"breakout_breakdown":bb,"support":support,"resistance":resistance},"trend":trend,"score":score,"trade_setup":setup,"data_status":"DEMO"}
