import Metric from "./Metric";
"use client";

import { useEffect, useState } from "react";

type MarketSessionData = {
  timezone: string;
  session: "OPEN" | "POST_MARKET" | "CLOSED";
  is_open: boolean;
  timestamp: string;
  market_open: string;
  market_close: string;
  next_session_open: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function MarketSession() {
  const [data, setData] = useState<MarketSessionData | null>(null);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        const response = await fetch(`${API_BASE}/api/v1/market/session`, {
          cache: "no-store",
        });
        if (!response.ok) return;

        const next = (await response.json()) as MarketSessionData;
        if (active) setData(next);
      } catch {
        // Keep the dashboard usable if the API is temporarily unavailable.
      }
    }

    load();
    const timer = setInterval(load, 30_000);

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, []);

  if (!data) {
    return <Metric label="Market Status" value="LOADING" change="Checking market session" />;
  }

  const change =
    data.session === "OPEN"
      ? `Closes ${data.market_close} IST`
      : data.session === "POST_MARKET"
        ? `Next session ${new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Kolkata" }).format(new Date(data.next_session_open))}`
        : `Next session ${new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Kolkata" }).format(new Date(data.next_session_open))}`;

  return (
    <Metric
      label="Market Status"
      value={data.session}
      change={change}
    />
  );
}
