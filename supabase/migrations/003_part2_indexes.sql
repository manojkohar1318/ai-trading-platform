-- Performance/index layer for the trading platform.
-- Safe to run after 001_initial.sql and 002_security_and_seed.sql.

create index if not exists idx_market_data_instrument_time
  on public.market_data (instrument_id, timestamp desc);

create index if not exists idx_candles_instrument_time
  on public.candles (instrument_id, timestamp desc);

create index if not exists idx_technical_indicators_instrument_time
  on public.technical_indicators (instrument_id, timestamp desc);

create index if not exists idx_signals_instrument_created
  on public.signals (instrument_id, created_at desc);

create index if not exists idx_predictions_instrument_created
  on public.predictions (instrument_id, created_at desc);

create index if not exists idx_backtests_strategy_created
  on public.backtests (strategy_id, created_at desc);
