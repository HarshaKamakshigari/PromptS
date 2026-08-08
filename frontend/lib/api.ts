import { HealthResponse, Metrics, Session, SessionDetail, DriftPoint, SecurityAlert } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }

  return res.json();
}

export const api = {
  getHealth: () => fetchAPI<HealthResponse>("/health"),
  
  getMetrics: () => fetchAPI<Metrics>("/metrics"),
  
  getSessions: (status?: string) => {
    const query = status ? `?status=${status}` : "";
    return fetchAPI<Session[]>(`/sessions${query}`);
  },
  
  getSession: (id: string) => fetchAPI<SessionDetail>(`/sessions/${id}`),
  
  getSessionDrift: (id: string) => fetchAPI<DriftPoint[]>(`/sessions/${id}/drift`),
  
  getAlerts: () => fetchAPI<SecurityAlert[]>("/alerts"),
};
