# Indian Trading AI — Part 1

Production-oriented foundation for an AI-powered Indian market analysis platform. **Part 1 uses explicitly labelled DEMO market data only**; it does not connect to brokers or place real trades.

## Stack
- Next.js + React + TypeScript + Tailwind-style CSS architecture
- FastAPI + Pydantic
- PostgreSQL/Supabase-compatible SQL migrations
- Python quantitative engine
- Recharts for terminal charts

## Run locally

### Web
```bash
cd apps/web
npm install
npm run dev
```
Open http://localhost:3000.

### API
```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Checks
```bash
npm run build
npm run lint
npm run typecheck
cd apps/api && python3 -m pytest tests
```

## Data safety
The mock provider returns synthetic data and the UI labels it `DEMO`. No API keys are committed and no real-money trading integration exists in Part 1.
