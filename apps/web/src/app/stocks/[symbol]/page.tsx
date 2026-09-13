"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Terminal from "@/components/Terminal";
import Link from "next/link";
import { getStock } from "@/lib/api";

export default function StockAnalyzer() {
  const params = useParams();
  const symbol = String(params?.symbol || "").toUpperCase();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!symbol) return;
    getStock(symbol).then(setData).catch((e) => setError(e.message));
  }, [symbol]);

  return (
    <Terminal title={`Stock Analyzer — ${symbol || "Select Stock"}`}>
      <div className="space-y-6">
        <div>
          <Link href="/stocks" className="muted text-sm">← Stocks</Link>
          <h1 className="text-3xl font-semibold mt-2">{symbol}</h1>
          <p className="muted mt-1">Quantitative analysis and trade setup engine</p>
        </div>

        {error && <div className="card p-5 text-red-300">{error}</div>}
        {!data && !error && <div className="card p-8 muted">Analyzing {symbol}…</div>}

        {data && (
          <>
            <div className="card p-6">
              <div className="flex flex-wrap justify-between gap-4">
                <div>
                  <div className="muted text-sm">Current Price</div>
                  <div className="text-3xl font-semibold">
                    ₹{Number(data.quote?.price ?? 0).toLocaleString("en-IN", { maximumFractionDigits: 2 })}
                  </div>
                </div>
                <div>
                  <div className="muted text-sm">Change</div>
                  <div className="text-xl font-semibold">
                    {Number(data.quote?.change_pct ?? 0).toFixed(2)}%
                  </div>
                </div>
                <div>
                  <div className="muted text-sm">Score</div>
                  <div className="text-3xl font-semibold">{data.score?.total_score ?? "—"}</div>
                </div>
                <div>
                  <div className="muted text-sm">Trend</div>
                  <div className="text-xl font-semibold uppercase">{data.trend ?? "—"}</div>
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="card p-5">
                <h2 className="font-semibold mb-4">Technical Indicators</h2>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  {Object.entries(data.indicators ?? {}).map(([key, value]) => (
                    <div key={key} className="border border-[#202938] rounded-lg p-3">
                      <div className="muted">{key.replaceAll("_", " ").toUpperCase()}</div>
                      <div className="font-medium mt-1">{Number(value).toFixed(2)}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card p-5">
                <h2 className="font-semibold mb-4">Structure & Levels</h2>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between"><span className="muted">Support</span><b>₹{Number(data.structure?.support ?? 0).toFixed(2)}</b></div>
                  <div className="flex justify-between"><span className="muted">Resistance</span><b>₹{Number(data.structure?.resistance ?? 0).toFixed(2)}</b></div>
                  <div className="flex justify-between"><span className="muted">Breakout</span><b>{data.structure?.breakout_breakdown ?? "none"}</b></div>
                  <div className="flex justify-between"><span className="muted">Higher Highs</span><b>{String(data.structure?.higher_highs)}</b></div>
                  <div className="flex justify-between"><span className="muted">Higher Lows</span><b>{String(data.structure?.higher_lows)}</b></div>
                </div>
              </div>
            </div>

            <div className="card p-5">
              <h2 className="font-semibold mb-4">Score Breakdown</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {Object.entries(data.score?.component_scores ?? {}).map(([key, value]) => (
                  <div key={key} className="border border-[#202938] rounded-lg p-4">
                    <div className="muted text-sm">{key.replaceAll("_", " ").toUpperCase()}</div>
                    <div className="text-xl font-semibold mt-1">{Number(value).toFixed(1)}/100</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-6">
              <h2 className="font-semibold text-lg">Trade Setup</h2>
              {data.trade_setup ? (
                <pre className="mt-4 text-sm overflow-auto">{JSON.stringify(data.trade_setup, null, 2)}</pre>
              ) : (
                <div className="mt-4">
                  <div className="text-xl font-semibold">NO TRADE SETUP</div>
                  <div className="muted mt-1">The engine did not identify a sufficiently defined setup.</div>
                </div>
              )}
            </div>

            <div className="card p-5">
              <div className="text-xs uppercase tracking-wide muted">
                {data.data_status || "DEMO"} DATA
              </div>
              <div className="muted text-sm mt-1">
                Analysis is informational only and does not guarantee trading outcomes.
              </div>
            </div>
          </>
        )}
      </div>
    </Terminal>
  );
}
