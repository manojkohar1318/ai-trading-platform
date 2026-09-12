"use client";

import { useEffect, useState } from "react";
import Terminal from "@/components/Terminal";
import { getMarketsOverview } from "@/lib/api";

type MarketRow = {
  symbol: string;
  price: number;
  change_percent: number;
  score?: number;
  trend?: string;
};

export default function MarketsPage() {
  const [data, setData] = useState<{ status?: string; stocks?: MarketRow[]; indices?: MarketRow[] } | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getMarketsOverview()
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <Terminal title="Markets">
      <div className="card p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">Markets</h1>
            <p className="muted mt-1">
              Indian market overview and quantitative snapshot.
            </p>
          </div>
          <span className="text-xs text-amber-300 border border-amber-500/30 rounded px-3 py-1">
            {data?.status || "LOADING"}
          </span>
        </div>

        {error && (
          <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300">
            {error}
          </div>
        )}

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {(data?.indices || []).map((index) => (
            <div key={index.symbol} className="rounded-xl border border-white/10 bg-black/20 p-5">
              <div className="text-sm muted">{index.symbol}</div>
              <div className="mt-2 text-2xl font-semibold">
                ₹{index.price?.toLocaleString("en-IN")}
              </div>
              <div className="mt-1 text-sm text-emerald-400">
                {index.change_percent?.toFixed(2)}%
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-left muted">
                <th className="p-3">Symbol</th>
                <th className="p-3">Price</th>
                <th className="p-3">Change</th>
                <th className="p-3">Score</th>
                <th className="p-3">Trend</th>
              </tr>
            </thead>
            <tbody>
              {(data?.stocks || []).map((stock) => (
                <tr key={stock.symbol} className="border-b border-white/5">
                  <td className="p-3 font-medium">{stock.symbol}</td>
                  <td className="p-3">₹{stock.price?.toLocaleString("en-IN")}</td>
                  <td className="p-3">{stock.change_percent?.toFixed(2)}%</td>
                  <td className="p-3">{stock.score ?? "—"}</td>
                  <td className="p-3">{stock.trend ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Terminal>
  );
}
