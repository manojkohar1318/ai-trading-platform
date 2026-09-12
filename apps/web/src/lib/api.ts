const API_BASE = "/backend";

export async function getMarketSession() {
  const response = await fetch(`${API_BASE}/api/v1/market/session`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Failed to load market session");
  return response.json();
}

export async function getProviderStatus() {
  const response = await fetch(`${API_BASE}/api/v1/providers/status`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Failed to load provider status");
  return response.json();
}

export async function getMarketsOverview() {
  const response = await fetch(`${API_BASE}/api/v1/markets/overview`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Failed to load markets overview");
  return response.json();
}
