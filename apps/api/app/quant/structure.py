from __future__ import annotations
from typing import Sequence

def support_resistance(close: Sequence[float], lookback: int=20):
    if not close: return None,None
    w=close[-lookback:]
    return min(w),max(w)

def price_structure(close: Sequence[float], lookback: int=5):
    if len(close)<lookback*2: return {"higher_highs":False,"higher_lows":False,"lower_highs":False,"lower_lows":False}
    a=close[-2*lookback:-lookback]; b=close[-lookback:]
    return {"higher_highs":max(b)>max(a),"higher_lows":min(b)>min(a),"lower_highs":max(b)<max(a),"lower_lows":min(b)<min(a)}

def breakout_breakdown(close: Sequence[float], lookback: int=20):
    if len(close)<=lookback: return "none"
    prior=close[-lookback-1:-1]; last=close[-1]
    if last>max(prior): return "breakout"
    if last<min(prior): return "breakdown"
    return "none"

def gap_pct(today_open: float, prev_close: float):
    return 0.0 if prev_close==0 else (today_open/prev_close-1)*100
