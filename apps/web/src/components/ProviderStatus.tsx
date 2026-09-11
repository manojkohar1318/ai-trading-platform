"use client";

import { useEffect, useState } from "react";
import { getProviderStatus } from "../lib/api";

type ProviderStatusData = {
  provider: string;
  description: string;
  implemented: boolean;
};

export default function ProviderStatus() {
  const [status, setStatus] = useState<ProviderStatusData | null>(null);

  useEffect(() => {
    getProviderStatus()
      .then(setStatus)
      .catch(() => setStatus(null));
  }, []);

  if (!status) return null;

  const isDemo = status.provider === "mock" || status.provider === "demo";

  return (
    <div className="mb-4 flex items-center justify-between rounded-lg border border-[#24313a] bg-[#0c121c] px-4 py-3">
      <div>
        <div className="text-xs uppercase tracking-wider text-[#7f8c96]">
          Market Data Provider
        </div>
        <div className="mt-1 text-sm font-medium">
          {status.provider.toUpperCase()}
        </div>
      </div>
      <div
        className={`rounded-full px-3 py-1 text-xs font-semibold ${
          isDemo
            ? "bg-amber-500/15 text-amber-300"
            : "bg-emerald-500/15 text-emerald-300"
        }`}
      >
        {isDemo ? "DEMO DATA" : "LIVE DATA"}
      </div>
    </div>
  );
}
