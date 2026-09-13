'use client';

import { useEffect, useMemo, useState } from 'react';
import Terminal from '@/components/Terminal';
import StockTable from '@/components/StockTable';
import { getScanner } from '@/lib/api';

type ScannerRow = {
  symbol: string;
  price: number;
  change_percent: number;
  score: number;
  trend: string;
  setup?: unknown;
};

export default function Scanner() {
  const [minScore, setMinScore] = useState(65);
  const [trend, setTrend] = useState('');
  const [data, setData] = useState<{ status?: string; results?: ScannerRow[]; message?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');

    getScanner(minScore, trend || undefined)
      .then((result) => {
        if (active) setData(result);
      })
      .catch((err) => {
        if (active) setError(err instanceof Error ? err.message : 'Failed to load scanner');
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [minScore, trend]);

  const rows = useMemo(
    () =>
      (data?.results ?? []).map((item) => [
        item.symbol,
        item.price,
        item.change_percent,
        item.score,
        item.trend,
      ]),
    [data],
  );

  return (
    <Terminal title="Scanner">
      <div className="space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold">Market Scanner</h1>
            <p className="muted mt-1 text-sm">
              Quantitative scan using the platform scoring and trade-setup engine.
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            <label className="text-xs muted">
              Minimum score
              <input
                aria-label="Minimum score"
                type="number"
                min="0"
                max="100"
                value={minScore}
                onChange={(e) => setMinScore(Number(e.target.value))}
                className="ml-2 w-20 rounded border border-[#263143] bg-[#0d131e] px-2 py-1 text-white"
              />
            </label>

            <label className="text-xs muted">
              Trend
              <select
                aria-label="Trend filter"
                value={trend}
                onChange={(e) => setTrend(e.target.value)}
                className="ml-2 rounded border border-[#263143] bg-[#0d131e] px-2 py-1 text-white"
              >
                <option value="">All</option>
                <option value="Bullish">Bullish</option>
                <option value="Bearish">Bearish</option>
                <option value="Neutral">Neutral</option>
              </select>
            </label>
          </div>
        </div>

        <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 px-3 py-2 text-xs text-amber-200">
          {data?.status === 'DEMO'
            ? 'DEMO DATA — scanner results are generated from the mock market provider.'
            : 'LIVE DATA — results are from the configured market-data provider.'}
        </div>

        {loading && <div className="card p-6 text-sm muted">Scanning instruments…</div>}

        {error && (
          <div className="card p-6 text-sm text-red-300">
            Scanner error: {error}
          </div>
        )}

        {!loading && !error && rows.length > 0 && <StockTable rows={rows} />}

        {!loading && !error && rows.length === 0 && (
          <div className="card p-8 text-center">
            <div className="text-lg font-medium">NO TRADE SETUP</div>
            <div className="muted mt-2 text-sm">
              {data?.message ?? 'No instrument meets the selected scanner criteria.'}
            </div>
          </div>
        )}
      </div>
    </Terminal>
  );
}
