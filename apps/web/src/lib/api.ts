const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getMarketSession() {
  const response = await fetch(`${API_BASE}/api/v1/market/session`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Failed to load market session");
  return response.json();
}
