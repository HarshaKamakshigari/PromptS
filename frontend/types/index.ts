// src/types/index.ts

export type SessionStatus = "active" | "safe" | "flagged" | "blocked";
export type Severity = "low" | "medium" | "high" | "critical";

export interface Metrics {
  requests: number;
  active_sessions: number;
  flagged: number;
  blocked: number;
  average_latency_ms: number;
  uptime: number;
}

export interface Session {
  id: string;
  provider: string;
  model: string;
  started_at: string;
  last_activity: string;
  status: SessionStatus;
  risk_score: number;
  request_count: number;
}

export interface DriftPoint {
  timestamp: string;
  semantic_drift: number;
  intent_drift: number;
  risk: number;
}

export interface Message {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface SessionDetail {
  session: Session;
  drift_timeline: DriftPoint[];
  messages: Message[];
}

export interface SecurityAlert {
  id: string;
  session_id: string;
  severity: Severity;
  type: string;
  score: number;
  action: string;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  provider: string;
  proxy: string;
}
