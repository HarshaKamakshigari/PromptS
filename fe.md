# PromptShield Frontend PRD

## Phase 1 — Security Observability + Live LLM Testing Console

**Version:** 1.0
**Author:** Harsha
**Date:** August 2026

---

# 1. Product Overview

PromptShield's frontend is a clean, minimal security observability dashboard combined with a live LLM testing console.

The application has two primary purposes:

1. **Chat with the LLM through PromptShield**
2. **Observe the resulting request/session metrics on the dashboard**

The frontend should make the PromptShield architecture visible:

```text
                    ┌──────────────┐
                    │   Chat UI    │
                    └──────┬───────┘
                           │
                           ▼
                  PromptShield Proxy
                           │
                           ▼
                         Groq
                           │
                           ▼
                    Response Stream
                           │
                           ├──────────────┐
                           ▼              ▼
                        Chat UI       Telemetry
                                         │
                                         ▼
                                    Dashboard
```

The user should be able to open the application, start a chat, send multiple messages, and immediately see the resulting request/session metrics reflected in the dashboard.

---

# 2. Product Philosophy

The interface should feel like:

> **A security engineering tool, not a generic AI chat application and not a generic admin dashboard.**

Design principles:

* Minimal
* Dark
* Technical
* Premium
* Dense but readable
* Fast
* No unnecessary decoration
* Strong typography
* Data-first
* Security-oriented

Avoid:

* Excessive gradients
* Giant colorful cards
* Excessive rounded corners
* Neon hacker aesthetics
* Unnecessary animations
* Generic SaaS dashboard patterns

---

# 3. Technology Stack

Use:

* Next.js
* TypeScript
* App Router
* Tailwind CSS
* shadcn/ui
* Recharts
* Lucide React

Font:

> **JetBrains Mono**

Use JetBrains Mono throughout the application.

The font should reinforce the developer/security tooling aesthetic.

---

# 4. Application Structure

```text
frontend/
│
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   │
│   ├── dashboard/
│   │   └── page.tsx
│   │
│   ├── chat/
│   │   └── page.tsx
│   │
│   ├── sessions/
│   │   ├── page.tsx
│   │   └── [id]/
│   │       └── page.tsx
│   │
│   ├── alerts/
│   │   └── page.tsx
│   │
│   └── settings/
│       └── page.tsx
│
├── components/
│   ├── layout/
│   │   ├── sidebar.tsx
│   │   ├── topbar.tsx
│   │   └── page-header.tsx
│   │
│   ├── dashboard/
│   │   ├── stat-card.tsx
│   │   ├── request-chart.tsx
│   │   ├── latency-chart.tsx
│   │   ├── drift-chart.tsx
│   │   ├── security-events.tsx
│   │   └── live-activity.tsx
│   │
│   ├── chat/
│   │   ├── chat-window.tsx
│   │   ├── message-list.tsx
│   │   ├── message-bubble.tsx
│   │   ├── chat-input.tsx
│   │   ├── session-header.tsx
│   │   └── connection-status.tsx
│   │
│   ├── sessions/
│   │   ├── session-table.tsx
│   │   ├── session-status.tsx
│   │   └── session-detail.tsx
│   │
│   ├── alerts/
│   │   ├── alert-table.tsx
│   │   ├── severity-badge.tsx
│   │   └── alert-detail.tsx
│   │
│   └── ui/
│
├── lib/
│   ├── api.ts
│   ├── chat.ts
│   ├── mock-data.ts
│   └── utils.ts
│
├── types/
│   └── index.ts
│
└── public/
```

---

# 5. Global Layout

Use a persistent left sidebar.

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PromptShield                                               │
│                                                             │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  Dashboard   │                                              │
│  Chat        │              Main Content                    │
│  Sessions    │                                              │
│  Alerts      │                                              │
│              │                                              │
│  ─────────   │                                              │
│  Settings    │                                              │
│              │                                              │
│              │                                              │
│              │                                              │
│  ● Groq      │                                              │
│    Online    │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

Sidebar should remain compact.

Navigation:

```text
Dashboard
Chat
Sessions
Alerts

────────────

Settings
```

Bottom:

```text
● Groq Connected
Proxy Online
```

---

# 6. Global Header

Topbar should show:

```text
PromptShield / Dashboard

                         ● Proxy Online
                         Groq
```

For the Chat page:

```text
PromptShield / Chat

                         ● Groq Connected
```

Keep the header quiet and minimal.

---

# 7. Dashboard

Route:

```text
/dashboard
```

This is the primary observability screen.

---

## 7.1 Dashboard Header

```text
Security Overview

Real-time activity through PromptShield

                         [Refresh]
```

Show connection status:

```text
● Proxy Online
```

---

# 8. Dashboard KPI Cards

Display four primary metrics.

### Requests

```text
12,482

REQUESTS
+12.4%
```

### Sessions

```text
184

ACTIVE SESSIONS
+8.2%
```

### Threats

```text
23

SECURITY EVENTS
```

### Latency

```text
42 ms

AVG LATENCY
```

Cards should be compact.

Don't make them huge.

---

# 9. Dashboard — Request Activity

Create a line/area-style chart using Recharts.

Title:

```text
Request Activity
```

Show:

* Requests
* Successful responses
* Failed responses

Time range:

```text
1H
6H
24H
7D
```

For Phase 1, use real backend metrics where available.

---

# 10. Dashboard — Latency

Display:

```text
Proxy Latency
```

Chart:

```text
ms
│
│       ╭╮
│   ╭───╯╰──╮
│───╯       ╰────
│
└─────────────────
```

Show:

* average latency
* p95 latency if available
* current latency

---

# 11. Dashboard — Drift Visualization

This is the future signature PromptShield visualization.

For Phase 1:

```text
Drift Monitoring
```

Show an empty/preview state:

```text
┌──────────────────────────────────────┐
│ Drift Monitoring                     │
│                                      │
│         Detection engine             │
│         not active                   │
│                                      │
│     Semantic drift                  │
│     Intent drift                    │
│     Risk score                      │
│                                      │
│         Coming in Phase 2            │
└──────────────────────────────────────┘
```

Do not fake security detections.

When Phase 2 is implemented, this component should automatically display:

```text
Semantic Drift
Intent Drift
Risk Score
Threshold
```

---

# 12. Dashboard — Recent Activity

Show real requests generated through the chat interface.

Example:

```text
Recent Activity

08:42:13   ps_8f21c9   llama-3.3-70b   1.2s
08:41:57   ps_72ab91   llama-3.3-70b   0.8s
08:41:32   ps_192fa1   llama-3.3-70b   1.1s
```

Clicking a row opens:

```text
/sessions/[id]
```

---

# 13. Dashboard — Security Events

Phase 1 will normally have no detection events.

Display:

```text
Security Events

No security events detected.

Detection monitoring will appear here
when the Phase 2 engine is enabled.
```

Once Phase 2 exists, display:

| Severity | Type           | Session   | Score | Action  |
| -------- | -------------- | --------- | ----: | ------- |
| HIGH     | Intent Drift   | `ps_8f21` |  0.91 | Blocked |
| MEDIUM   | Semantic Drift | `ps_72ab` |  0.68 | Flagged |

---

# 14. Chat Page

Route:

```text
/chat
```

This is extremely important.

It acts as the **live testing console for PromptShield**.

The user should be able to send prompts directly through the PromptShield proxy.

---

# 15. Chat Layout

Use a split layout.

```text
┌────────────────────────────────────────────────────────────┐
│ Chat                                      Session #ps_8f21 │
├───────────────────────────────────────┬────────────────────┤
│                                       │                    │
│ User                                  │ SESSION            │
│ Explain Kubernetes networking         │                    │
│                                       │ Model              │
│ Assistant                             │ llama-3.3-70b      │
│ Kubernetes networking allows...       │                    │
│                                       │ Provider           │
│ User                                  │ Groq               │
│ What are services?                    │                    │
│                                       │ Status             │
│ Assistant                             │ ● Active           │
│ ...                                   │                    │
│                                       │ Requests           │
│                                       │ 4                  │
│                                       │                    │
│                                       │ Latency            │
│                                       │ 821 ms             │
├───────────────────────────────────────┴────────────────────┤
│ Type a message...                              [Send ↑]    │
└────────────────────────────────────────────────────────────┘
```

---

# 16. Chat Session

Every chat page should have a session.

When the user opens Chat:

```text
Create session
```

or lazily create it on the first message.

Session ID:

```text
ps_<unique-id>
```

Example:

```text
ps_8f21c9
```

Display it in the chat header.

---

# 17. Chat Header

Example:

```text
Chat

● Groq Connected
llama-3.3-70b-versatile

Session
ps_8f21c9
```

Include:

```text
[New Session]
```

button.

---

# 18. Chat Messages

Messages should be visually minimal.

### User

```text
┌──────────────────────────────────────────┐
│ USER                                     │
│ Explain Kubernetes networking.           │
└──────────────────────────────────────────┘
```

### Assistant

```text
ASSISTANT

Kubernetes networking provides...
```

Don't use giant colorful chat bubbles.

Use typography and subtle borders.

---

# 19. Streaming

The chat must support streaming responses.

Flow:

```text
Chat Input
    ↓
POST /v1/chat/completions
    ↓
PromptShield
    ↓
Groq
    ↓
SSE stream
    ↓
Chat UI
```

Assistant text should appear token/chunk by chunk.

Show:

```text
ASSISTANT
Kubernetes networking provides...
                              ▌
```

while streaming.

---

# 20. Chat Input

Bottom-fixed input.

```text
┌────────────────────────────────────────────────────┐
│ Message PromptShield...                       ↑    │
└────────────────────────────────────────────────────┘
```

Features:

* Enter → send
* Shift + Enter → newline
* Disabled while appropriate
* Loading/streaming state
* Stop generation button

During streaming:

```text
[Stop]
```

---

# 21. Chat Controls

Small controls near the input:

```text
Model: llama-3.3-70b-versatile
Streaming: ON
```

Don't expose unnecessary provider settings.

---

# 22. Live Session Telemetry

The right panel should update after every request.

Example:

```text
SESSION

ps_8f21c9

Provider
Groq

Model
llama-3.3-70b-versatile

Messages
8

Requests
4

Avg latency
742 ms

Status
● Active
```

Later:

```text
Risk
0.18

Semantic drift
0.12

Intent drift
0.07
```

---

# 23. Chat → Dashboard Integration

This is one of the most important requirements.

When a user sends:

```text
Explain Kubernetes.
```

PromptShield creates a request/session event.

The dashboard must reflect it.

Example:

Before:

```text
Requests
42
```

After sending:

```text
Requests
43
```

Session count updates if a new session was created.

Latency updates after completion.

Recent activity gets a new entry.

---

# 24. Real-Time Updates

Phase 1 does not require WebSockets.

Use polling.

Dashboard can refresh metrics every:

```text
5–10 seconds
```

or refresh after chat completion.

Architecture:

```text
Chat
 ↓
Backend
 ↓
Session updated
 ↓
Frontend refresh
 ↓
Dashboard reflects new data
```

Later, WebSockets/SSE can provide real-time telemetry.

---

# 25. Sessions Page

Route:

```text
/sessions
```

Display:

```text
Sessions

Search...

┌────────────┬────────────┬─────────────┬──────────┬─────────┐
│ Session    │ Provider   │ Model       │ Requests │ Status  │
├────────────┼────────────┼─────────────┼──────────┼─────────┤
│ ps_8f21c9  │ Groq       │ llama-3.3   │ 4        │ ACTIVE  │
│ ps_72ab91  │ Groq       │ llama-3.3   │ 2        │ SAFE    │
└────────────┴────────────┴─────────────┴──────────┴─────────┘
```

Click:

```text
ps_8f21c9
```

→ `/sessions/ps_8f21c9`

---

# 26. Session Detail

Show:

```text
Session ps_8f21c9

● ACTIVE

Provider
Groq

Model
llama-3.3-70b-versatile

Started
08:42:13

Requests
4

Average latency
742ms
```

Then:

### Conversation

Show the full conversation.

### Request Timeline

```text
Request 1     812ms
Request 2     693ms
Request 3     721ms
Request 4     742ms
```

### Drift

Phase 1:

```text
Detection engine inactive.
```

Phase 2:

Actual drift chart.

---

# 27. Alerts Page

Route:

```text
/alerts
```

Phase 1 empty state:

```text
No security alerts

PromptShield has not detected
any security events yet.
```

Do not fabricate threats simply to make the UI look populated.

---

# 28. Settings Page

Route:

```text
/settings
```

Display:

### Proxy

```text
Status
● Online

Endpoint
http://localhost:8000
```

### Provider

```text
Provider
Groq

Endpoint
api.groq.com

Status
● Connected
```

### Model

```text
llama-3.3-70b-versatile
```

### Detection

```text
Semantic Detection
○ Disabled

Intent Detection
○ Disabled

Risk Engine
○ Disabled

Phase 2
```

---

# 29. API Layer

Create:

```text
lib/api.ts
```

Functions:

```typescript
getHealth()
getMetrics()
getSessions()
getSession(id)
getSessionDrift(id)
getAlerts()
```

Create:

```text
lib/chat.ts
```

Responsible for:

```text
sendChatMessage()
streamChatResponse()
```

Keep chat streaming logic separate from normal REST API calls.

---

# 30. Environment Variables

Create:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Never put:

```text
GROQ_API_KEY
```

in the frontend.

The frontend must never communicate directly with Groq.

Correct:

```text
Browser
 ↓
PromptShield
 ↓
Groq
```

Incorrect:

```text
Browser
 ↓
Groq
```

---

# 31. TypeScript Types

Create:

```text
types/index.ts
```

Define:

```typescript
type SessionStatus =
  | "active"
  | "safe"
  | "flagged"
  | "blocked";

type Severity =
  | "low"
  | "medium"
  | "high"
  | "critical";

interface Metrics {
  requests: number;
  active_sessions: number;
  flagged: number;
  blocked: number;
  average_latency_ms: number;
  uptime: number;
}

interface Session {
  id: string;
  provider: string;
  model: string;
  started_at: string;
  last_activity: string;
  status: SessionStatus;
  risk_score: number;
}

interface DriftPoint {
  timestamp: string;
  semantic_drift: number;
  intent_drift: number;
  risk: number;
}

interface SecurityAlert {
  id: string;
  session_id: string;
  severity: Severity;
  type: string;
  score: number;
  action: string;
  timestamp: string;
}
```

Use the backend's actual response shape if it differs.

---

# 32. Design System

## Font

Use:

```text
JetBrains Mono
```

throughout.

Do not mix several fonts.

---

## Background

Use a near-black background.

```text
#09090B
```

---

## Surface

Cards:

```text
#111113
```

---

## Borders

Use subtle neutral borders.

Avoid heavy outlines.

---

## Typography

Primary:

```text
#F4F4F5
```

Secondary:

```text
#A1A1AA
```

Muted:

```text
#71717A
```

---

# 33. Color Usage

Keep the interface mostly monochrome.

Use semantic colors only when necessary:

```text
Green  → healthy / safe
Yellow → warning
Orange → high risk
Red    → blocked / critical
```

Do not turn the entire dashboard into a rainbow.

---

# 34. Visual Style

Use:

* thin borders
* subtle shadows
* small radius
* compact cards
* monospace metrics
* simple icons
* restrained hover states
* subtle transitions

Avoid:

* giant rounded cards
* excessive blur
* glassmorphism
* animated gradients
* huge hero sections

The product should feel like a serious security tool.

---

# 35. Responsive Design

Desktop is the primary target.

Still support:

### Tablet

Sidebar can collapse.

### Mobile

Use:

```text
top navigation
```

and stack charts vertically.

Chat should remain usable on mobile.

---

# 36. Loading States

Every API-backed component needs a loading state.

Example:

```text
Loading metrics...
```

Use subtle skeletons rather than spinners everywhere.

---

# 37. Error States

Backend unavailable:

```text
PromptShield backend unavailable

Unable to connect to
http://localhost:8000

[Retry]
```

Groq unavailable:

```text
Groq connection failed

Check the PromptShield backend
and upstream provider configuration.
```

---

# 38. Empty States

Do not display fake data when real data is unavailable.

Example:

```text
No sessions yet

Start a conversation in Chat
to create your first PromptShield session.

[Open Chat]
```

This creates a natural flow:

```text
Dashboard
   ↓
No sessions
   ↓
Open Chat
   ↓
Send message
   ↓
Session created
   ↓
Dashboard populated
```

---

# 39. Dashboard Live Flow

The primary demo should work like this:

### Step 1

Open:

```text
/dashboard
```

Initially:

```text
Requests: 0
Sessions: 0
```

### Step 2

Go to:

```text
/chat
```

### Step 3

Send:

```text
Explain Kubernetes networking.
```

### Step 4

PromptShield sends request to Groq.

### Step 5

Response streams into the chat.

### Step 6

Backend records:

```text
request
session
latency
model
provider
```

### Step 7

Return to Dashboard.

It now shows:

```text
Requests: 1
Sessions: 1
Latency: 742ms
```

### Step 8

Send more messages.

Dashboard updates accordingly.

This should be the main Phase 1 demonstration.

---

# 40. Phase 1 Acceptance Criteria

## Chat

* [ ] Chat page works.
* [ ] User can create a session.
* [ ] User can send messages.
* [ ] Messages are sent through PromptShield.
* [ ] Groq response streams into the UI.
* [ ] Stop generation works where supported.
* [ ] Multiple turns work.
* [ ] Session ID is displayed.
* [ ] Provider/model are displayed.
* [ ] No Groq API key exists in browser code.

## Dashboard

* [ ] Dashboard loads backend metrics.
* [ ] Request count updates.
* [ ] Session count updates.
* [ ] Latency displays.
* [ ] Proxy health displays.
* [ ] Recent activity displays.
* [ ] Charts render correctly.
* [ ] Empty states are clean.

## Sessions

* [ ] Sessions list loads.
* [ ] Session detail loads.
* [ ] Conversation is visible.
* [ ] Request history is visible.
* [ ] Drift component exists.

## Alerts

* [ ] Alerts endpoint is connected.
* [ ] Empty state works.
* [ ] Future detection alerts can be rendered without redesign.

## Settings

* [ ] Backend health is visible.
* [ ] Groq connection is visible.
* [ ] Current model is visible.
* [ ] Detection status is visible.

---

# 41. Phase 1 Must NOT Implement

Do not implement:

* semantic embeddings
* MiniLM
* semantic drift
* intent classification
* risk scoring
* automatic blocking
* prompt injection detection
* WebSockets
* authentication
* database

These belong to later phases.

The frontend should only provide the **visual slots** for these capabilities.

---

# 42. Phase 2 Frontend Preparation

The frontend should already have components ready for:

```text
DriftChart
RiskScore
DetectionEvent
IntentAnalysis
PolicyDecision
```

When Phase 2 backend APIs become available, they should plug into existing components.

---

# 43. Final User Experience

The finished Phase 1 application should feel like:

```text
┌──────────────────────────────────────────────────────┐
│ PromptShield                       ● Proxy Online    │
├────────────┬─────────────────────────────────────────┤
│            │                                         │
│ Dashboard  │  Security Overview                     │
│            │                                         │
│ Chat       │  12,482       184        42ms           │
│            │  Requests     Sessions   Latency        │
│ Sessions   │                                         │
│            │  ┌─────────────────────────────────┐    │
│ Alerts     │  │ Request Activity                │    │
│            │  │          ╭────╮                 │    │
│            │  │     ╭────╯    ╰───              │    │
│            │  └─────────────────────────────────┘    │
│            │                                         │
│            │  ┌─────────────────────────────────┐    │
│            │  │ Drift Monitoring                │    │
│            │  │      Detection coming Phase 2   │    │
│            │  └─────────────────────────────────┘    │
│            │                                         │
│            │  Recent Activity                        │
│            │  ps_8f21c9   Groq   742ms              │
│            │  ps_72ab91   Groq   681ms              │
│            │                                         │
└────────────┴─────────────────────────────────────────┘
```

And the live testing experience:

```text
┌──────────────────────────────────────────────────────┐
│ Chat                         ● Groq Connected         │
├──────────────────────────────────┬───────────────────┤
│                                  │ Session           │
│ USER                             │                   │
│ Explain Kubernetes networking.   │ ps_8f21c9         │
│                                  │                   │
│ ASSISTANT                        │ Model             │
│ Kubernetes networking allows...  │ llama-3.3-70b     │
│                                  │                   │
│ USER                             │ Requests          │
│ What are services?               │ 2                 │
│                                  │                   │
│ ASSISTANT                        │ Avg latency       │
│ Services provide...             │ 742ms             │
│                                  │                   │
├──────────────────────────────────┴───────────────────┤
│ Message PromptShield...                         ↑    │
└──────────────────────────────────────────────────────┘
```

---

# 44. Core Principle

The frontend should make one thing extremely obvious:

> **Every conversation through PromptShield becomes observable security telemetry.**

The user chats normally.

PromptShield handles the request.

Groq generates the response.

The session becomes telemetry.

The dashboard visualizes it.

Later, the exact same interface will show:

```text
Normal conversation
       ↓
Semantic drift
       ↓
Intent drift
       ↓
Risk increase
       ↓
Security alert
       ↓
Policy decision
```

That transition from **LLM chat → observable behavior → security detection** is the central UX of PromptShield.
