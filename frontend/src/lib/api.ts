export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || `${BACKEND_URL}/api`;
export async function fetchProjectOverview() {
  const res = await fetch(`${API_BASE_URL}/project`, { next: { revalidate: 10 } });
  if (!res.ok) throw new Error("Failed to fetch project overview");
  return res.json();
}

export async function fetchArchitecture() {
  const res = await fetch(`${API_BASE_URL}/architecture`, { next: { revalidate: 10 } });
  if (!res.ok) throw new Error("Failed to fetch architecture");
  return res.json();
}

export async function fetchResults() {
  const res = await fetch(`${API_BASE_URL}/results`, { next: { revalidate: 1 } }); // fast revalidate for dashboard
  if (!res.ok) throw new Error("Failed to fetch results");
  return res.json();
}

export async function fetchDatasets() {
  const res = await fetch(`${API_BASE_URL}/datasets`, { next: { revalidate: 10 } });
  if (!res.ok) throw new Error("Failed to fetch datasets");
  return res.json();
}

export async function runLiveDemo(question: string) {
  const res = await fetch(`${API_BASE_URL}/demo`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to run demo");
  return res.json();
}
