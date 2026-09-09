# Architecture

```text
Browser (Next.js)
   ↓ typed HTTP client
FastAPI API
   ├─ market providers → MockMarketDataProvider / future real provider
   ├─ validation
   ├─ quant engine (indicators + structure)
   ├─ scoring engine
   ├─ trade setup engine
   ├─ scanner
   ├─ backtesting engine
   └─ AI orchestration (LLM provider abstraction)
          ↓
 PostgreSQL / Supabase
```

The LLM is an explanation/orchestration layer. Deterministic indicators, scores, trade levels and backtest metrics are calculated outside the LLM.
