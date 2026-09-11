from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .services.provider_factory import build_market_data_provider
from .services.analyzer import analyze
from .services.ai import MockLLMProvider, TradingAIService
from .services.risk import RiskInput, calculate_position_size
from .services.market_session import market_session

app = FastAPI(title="Indian Trading AI API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
provider = build_market_data_provider()
ai = TradingAIService(MockLLMProvider())

def quote_dict(q):
    return {"symbol":q.symbol,"price":q.price,"open":q.open,"high":q.high,"low":q.low,
            "previous_close":q.prev_close,"volume":q.volume,"change_percent":q.change_pct,"is_demo":q.is_demo}

@app.get("/health")
def health():
    return {"status":"ok","data_status":"DEMO" if getattr(provider,"is_demo",True) else "LIVE"}

@app.get("/api/v1/stocks/{symbol}")
def stock(symbol: str):
    try: return analyze(provider, symbol.upper())
    except Exception as exc: raise HTTPException(400,"Unable to analyze instrument") from exc

@app.get("/api/v1/stocks/{symbol}/candles")
def candles(symbol: str, limit: int = Query(100, ge=10, le=500)):
    try:
        rows = provider.get_ohlc(symbol.upper(), limit)
        return {"symbol":symbol.upper(),"candles":[c.__dict__ for c in rows],"data_status":"DEMO"}
    except Exception as exc: raise HTTPException(400,"Unable to load candles") from exc

@app.get("/api/v1/markets/overview")
def markets():
    rows=[]
    for symbol in provider.symbols:
        a=analyze(provider,symbol)
        rows.append(quote_dict(provider.get_quote(symbol)) | {"score":a["score"]["total_score"],"trend":a["trend"]})
    return {"status":"DEMO","data_status":"DEMO",
            "indices":[quote_dict(provider.get_index_data("NIFTY")),quote_dict(provider.get_index_data("BANKNIFTY"))],
            "breadth":provider.get_market_breadth(),"stocks":rows}

@app.get("/api/v1/markets/quotes")
def quotes():
    return {"status":"DEMO","quotes":[quote_dict(provider.get_quote(s)) for s in provider.symbols]}

@app.get("/api/v1/scanner")
def scanner(min_score: float=Query(0,ge=0,le=100), trend: str|None=None, limit: int=Query(10,ge=1,le=50)):
    results=[]
    for symbol in provider.symbols:
        a=analyze(provider,symbol)
        if a["score"]["total_score"] < min_score: continue
        if trend and a["trend"].lower()!=trend.lower(): continue
        if a["trade_setup"]:
            results.append({"symbol":symbol,"price":a["quote"]["price"],"change_percent":a["quote"]["change_pct"],
                            "score":a["score"]["total_score"],"trend":a["trend"],"setup":a["trade_setup"]})
    results.sort(key=lambda x:x["score"],reverse=True)
    return {"status":"DEMO","results":results[:limit],"message":None if results else "NO TRADE SETUP"}

@app.post("/api/v1/risk")
def risk(payload: RiskInput):
    try: return calculate_position_size(payload)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc

@app.post("/api/v1/assistant")
def assistant(payload: dict):
    q=str(payload.get("question","")).strip()
    if not q: raise HTTPException(422,"question is required")
    return {"answer":ai.answer(q),"data_status":"DEMO",
            "facts":[],"calculations":[],"estimates":[],
            "warnings":["AI provider is not configured; this is a DEMO response."]}


@app.get("/api/v1/market/session")
def session():
    return market_session()
