# Part 2 update package

This is an OVERLAY for the existing `ai-trading-platform` repository.
It is not a second application.

## Apply
1. Keep the repository's `.git` directory.
2. Extract the contents of this ZIP into `/workspaces/ai-trading-platform`.
3. Allow existing files to be replaced when prompted.
4. Do not delete unrelated project files.
5. Run the validation commands from the project root.

## Validation
Backend:
```bash
cd apps/api
python -m compileall app
PYTHONPATH=. pytest -q
```

Frontend:
```bash
cd apps/web
npm install
npm run lint
npm run build
```

## Data safety
The new HTTP adapter is vendor-neutral and does not invent a broker endpoint.
Until `MARKET_DATA_PROVIDER` is changed and a real gateway is configured,
the application remains in DEMO mode.

Never put a market-data API key in the Next.js client or browser environment.
