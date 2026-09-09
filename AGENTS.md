# AI Agent Instructions

- Preserve the separation between `apps/web`, `apps/api`, `packages/shared`, and `supabase`.
- Never expose secrets to client-side code; only `NEXT_PUBLIC_*` variables may be browser-visible.
- Treat all market-provider output as untrusted until validated by the API/data-validation layer.
- Mock market data must remain visibly labelled DEMO. Never describe it as live NSE/BSE data.
- Quantitative calculations belong in `apps/api/app/quant`; do not duplicate formulas in React.
- Trade setup numbers are estimates produced by deterministic rules, not LLM output.
- Do not add brokerage/order-placement functionality without an explicit future project phase.
- Add tests for every new quantitative formula and API contract.
- Prefer reusable UI components over page-specific duplication.
- Update README/ARCHITECTURE when changing major boundaries or environment variables.
