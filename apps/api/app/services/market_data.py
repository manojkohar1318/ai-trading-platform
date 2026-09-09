from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
import random
from datetime import datetime, timedelta, timezone

@dataclass
class Quote:
    symbol: str; price: float; open: float; high: float; low: float; prev_close: float; volume: int; change_pct: float; is_demo: bool=True

@dataclass
class Candle:
    timestamp: str; open: float; high: float; low: float; close: float; volume: int

class MarketDataProvider(ABC):
    @abstractmethod
    def get_quote(self,symbol:str)->Quote: ...
    @abstractmethod
    def get_ohlc(self,symbol:str,limit:int=100)->list[Candle]: ...
    @abstractmethod
    def get_intraday_candles(self,symbol:str,limit:int=100)->list[Candle]: ...
    @abstractmethod
    def get_historical_data(self,symbol:str,limit:int=252)->list[Candle]: ...
    @abstractmethod
    def get_index_data(self,symbol:str)->Quote: ...
    @abstractmethod
    def get_market_breadth(self)->dict: ...

class MockMarketDataProvider(MarketDataProvider):
    symbols={"RELIANCE":2780.0,"HDFCBANK":1740.0,"ICICIBANK":1450.0,"INFY":1850.0,"TCS":4250.0,"SBIN":820.0,"ITC":510.0,"LT":3900.0,"TATAMOTORS":720.0,"AXISBANK":1220.0}
    def _series(self,symbol,limit=100):
        base=self.symbols.get(symbol.upper(),1000.0); rng=random.Random(sum(map(ord,symbol)))
        out=[]; price=base*0.92; now=datetime.now(timezone.utc)
        for i in range(limit):
            drift=0.0012 if symbol.upper() in {"RELIANCE","ICICIBANK","SBIN"} else 0.0003
            change=rng.gauss(drift,0.012); o=price; c=max(1,price*(1+change)); h=max(o,c)*(1+rng.random()*0.006); l=min(o,c)*(1-rng.random()*0.006); v=int(500000+rng.random()*4000000)
            out.append(Candle((now-timedelta(minutes=(limit-i)*5)).isoformat(),o,h,l,c,v)); price=c
        return out
    def get_quote(self,symbol):
        c=self._series(symbol,2); last,prev=c[-1],c[-2]; return Quote(symbol.upper(),last.close,last.open,last.high,last.low,prev.close,last.volume,(last.close/prev.close-1)*100,True)
    def get_ohlc(self,symbol,limit=100): return self._series(symbol,limit)
    def get_intraday_candles(self,symbol,limit=100): return self._series(symbol,limit)
    def get_historical_data(self,symbol,limit=252): return self._series(symbol,limit)
    def get_index_data(self,symbol):
        bases={"NIFTY":24900,"BANKNIFTY":54000}; return Quote(symbol,bases.get(symbol,10000),bases.get(symbol,10000)*.998,bases.get(symbol,10000)*1.005,bases.get(symbol,10000)*.995,bases.get(symbol,10000)*.998,10000000,.2,True)
    def get_market_breadth(self): return {"advances":1267,"declines":941,"unchanged":122,"is_demo":True}
