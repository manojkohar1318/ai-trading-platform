from __future__ import annotations
import math
from statistics import stdev
from typing import Sequence

def sma(values: Sequence[float], period: int) -> list[float | None]:
    if period <= 0: raise ValueError("period must be positive")
    out=[]
    for i in range(len(values)):
        out.append(sum(values[i-period+1:i+1])/period if i+1>=period else None)
    return out

def ema(values: Sequence[float], period: int) -> list[float | None]:
    if period <= 0: raise ValueError("period must be positive")
    out=[None]*len(values)
    if len(values)<period: return out
    prev=sum(values[:period])/period; out[period-1]=prev; k=2/(period+1)
    for i in range(period,len(values)):
        prev=(values[i]-prev)*k+prev; out[i]=prev
    return out

def rsi(values: Sequence[float], period: int=14) -> list[float | None]:
    if len(values)<period+1: return [None]*len(values)
    gains=[]; losses=[]
    for i in range(1,len(values)):
        d=values[i]-values[i-1]; gains.append(max(d,0)); losses.append(max(-d,0))
    ag=sum(gains[:period])/period; al=sum(losses[:period])/period
    out=[None]*(period); out.append(100.0 if al==0 else 100-100/(1+ag/al))
    for i in range(period,len(gains)):
        ag=(ag*(period-1)+gains[i])/period; al=(al*(period-1)+losses[i])/period
        out.append(100.0 if al==0 else 100-100/(1+ag/al))
    return out

def macd(values: Sequence[float], fast: int=12, slow: int=26, signal: int=9):
    ef=ema(values,fast); es=ema(values,slow)
    line=[None if a is None or b is None else a-b for a,b in zip(ef,es)]
    clean=[x for x in line if x is not None]; sig_clean=ema(clean,signal)
    sig=[None]*len(line); idx=0
    for i,x in enumerate(line):
        if x is not None:
            sig[i]=sig_clean[idx]; idx+=1
    hist=[None if a is None or b is None else a-b for a,b in zip(line,sig)]
    return line,sig,hist

def roc(values: Sequence[float], period: int=12):
    return [None if i<period else (values[i]/values[i-period]-1)*100 for i in range(len(values))]

def atr(high: Sequence[float], low: Sequence[float], close: Sequence[float], period: int=14):
    tr=[]
    for i in range(len(close)):
        tr.append(high[i]-low[i] if i==0 else max(high[i]-low[i],abs(high[i]-close[i-1]),abs(low[i]-close[i-1])))
    return sma(tr,period)

def historical_volatility(values: Sequence[float], period: int=20, annualization: int=252):
    returns=[None]+[math.log(values[i]/values[i-1]) for i in range(1,len(values))]
    out=[]
    for i in range(len(values)):
        window=[x for x in returns[max(0,i-period+1):i+1] if x is not None]
        out.append(stdev(window)*math.sqrt(annualization)*100 if len(window)>=2 else None)
    return out

def vwap(high, low, close, volume):
    cum_pv=0.0; cum_v=0.0; out=[]
    for h,l,c,v in zip(high,low,close,volume):
        cum_pv += ((h+l+c)/3)*v; cum_v += v; out.append(cum_pv/cum_v if cum_v else None)
    return out

def relative_volume(volume, period=20):
    av=sma(volume,period); return [None if a is None or a==0 else v/a for v,a in zip(volume,av)]

def volume_breakout(volume, period=20, multiplier=1.5):
    av=sma(volume,period); return [a is not None and v>=a*multiplier for v,a in zip(volume,av)]

def ema_crossover(values, fast=9, slow=21):
    f=ema(values,fast); s=ema(values,slow); out=[]
    for i in range(len(values)):
        if i==0 or f[i] is None or s[i] is None or f[i-1] is None or s[i-1] is None: out.append("neutral")
        elif f[i]>s[i] and f[i-1]<=s[i-1]: out.append("bullish_cross")
        elif f[i]<s[i] and f[i-1]>=s[i-1]: out.append("bearish_cross")
        else: out.append("neutral")
    return out
