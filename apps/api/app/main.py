from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services.market_data import MockMarketDataProvider
from .services.analyzer import analyze
from .services.ai import MockLLMProvider,TradingAIService

app=FastAPI(title="Indian Trading AI API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
provider=MockMarketDataProvider(); ai=TradingAIService(MockLLMProvider())
@app.get("/health")
def health(): return {"status":"ok","data_status":"DEMO"}
@app.get("/api/v1/stocks/{symbol}")
def stock(symbol:str):
    try: return analyze(provider,symbol.upper())
    except Exception as e: raise HTTPException(400,"Unable to analyze instrument") from e
@app.get("/api/v1/markets/overview")
def markets():
    symbols=list(provider.symbols); rows=[analyze(provider,s)["quote"] | {"score":analyze(provider,s)["score"]["total_score"],"trend":analyze(provider,s)["trend"]} for s in symbols]
    return {"status":"DEMO","indices":[provider.get_index_data("NIFTY").__dict__,provider.get_index_data("BANKNIFTY").__dict__],"breadth":provider.get_market_breadth(),"stocks":rows}
@app.get("/api/v1/scanner")
def scanner():
    rows=[]
    for s in provider.symbols:
        a=analyze(provider,s); setup=a["trade_setup"]
        if setup: rows.append({"symbol":s,"price":a["quote"]["price"],"change_pct":a["quote"]["change_pct"],"score":a["score"]["total_score"],"trend":a["trend"],"setup":setup})
    rows.sort(key=lambda x:x["score"],reverse=True)
    return {"status":"DEMO","results":rows[:10],"message":None if rows else "NO TRADE SETUP"}
@app.post("/api/v1/assistant")
def assistant(payload:dict):
    q=str(payload.get("question","")).strip()
    if not q: raise HTTPException(422,"question is required")
    return {"answer":ai.answer(q),"data_status":"DEMO"}
