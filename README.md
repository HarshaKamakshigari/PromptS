# PromptShield

> Semantic & Intent Drift Detection Proxy for LLM Applications

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt

# Add your Groq API key to .env
# GROQ_API_KEY=gsk_...

uvicorn app.main:app --reload --port 8000
```

### Verify

```bash
# Health check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics

# Sessions
curl http://localhost:8000/sessions

# Alerts
curl http://localhost:8000/alerts
```

### Test with Groq

```python
from groq import Groq

client = Groq(
    api_key="gsk_...",
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Docker

```bash
cd backend
docker compose up
```

## Architecture

```
Application → PromptShield (localhost:8000) → Groq
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/metrics` | GET | Dashboard metrics |
| `/sessions` | GET | List sessions |
| `/sessions/{id}` | GET | Session detail |
| `/sessions/{id}/drift` | GET | Drift timeline |
| `/alerts` | GET | Security alerts |
| `/v1/chat/completions` | POST | Proxy endpoint |
