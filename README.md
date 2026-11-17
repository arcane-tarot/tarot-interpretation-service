# Tarot Interpretation Service — Backend

FastAPI service that receives a tarot card and the user's question, builds a
contextual prompt, and requests an interpretation from the OpenAI Responses
API. The code separates domain, use cases, HTTP adapters, and infrastructure.

## Requirements

- Python 3.13 and `make` for local development, or Docker and Docker Compose.
- An OpenAI API key with API access and billing enabled.

A ChatGPT subscription and OpenAI API billing are separate. This backend needs
an API key; it cannot reuse a ChatGPT browser session.

## Run the complete application with Docker Compose

From the parent `tarot` directory:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY.
docker compose up --build
```

- Frontend: <http://localhost:5174>
- Backend: <http://localhost:8000>
- Interactive API docs: <http://localhost:8000/docs>

Stop the stack with `docker compose down`.

## Run the backend locally

```bash
make install
cp .env.example .env
# Edit .env and set OPENAI_API_KEY.
make run
```

The server listens on `http://localhost:8000`.

## Configuration

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Empty | Secret used to authenticate with OpenAI. |
| `OPENAI_BASE_URL` | No | `https://api.openai.com/v1` | API base URL. |
| `OPENAI_MODEL` | No | `gpt-4.1-mini` | Interpretation model. |
| `OPENAI_TIMEOUT_SECONDS` | No | `20` | Upstream timeout. |
| `ALLOWED_ORIGINS` | No | Local port `5174` | Comma-separated CORS origins. |

Keep `.env` out of source control. Commit only `.env.example` without real
credentials.

## API

### Create an interpretation

```http
POST /api/tarot/interpretations
Content-Type: application/json
```

```json
{
  "question": "¿Qué necesito entender sobre esta decisión?",
  "deckType": "major",
  "card": {
    "name": "El Mago",
    "type": "major",
    "label": "Arcano mayor",
    "baseMeaning": "Voluntad, recursos y acción enfocada."
  }
}
```

Successful response:

```json
{
  "cardName": "El Mago",
  "interpretation": "..."
}
```

If the key is missing or OpenAI cannot be reached, the endpoint returns HTTP
`503`.

```bash
curl --fail --silent --show-error \
  -X POST http://localhost:8000/api/tarot/interpretations \
  -H 'Content-Type: application/json' \
  -d '{"question":"¿Qué necesito entender hoy?","deckType":"major","card":{"name":"El Mago","type":"major","label":"Arcano mayor","baseMeaning":"Voluntad y acción."}}'
```

## Health checks

| Endpoint | Meaning |
| --- | --- |
| `GET /health` | Basic service response. |
| `GET /health/live` | Process is alive. |
| `GET /health/startup` | Application started. |
| `GET /health/ready` | OpenAI API key is configured. |
| `GET /metrics` | Prometheus metrics for the backend. |

Readiness returns HTTP `503` when `OPENAI_API_KEY` is absent.

## Development

```bash
make format
make lint
make test
make docker-build
```

```text
app/
├── adapters/http/          # FastAPI routes and schemas
├── application/            # Commands, ports, results, and use cases
├── domain/                 # Tarot domain models
├── infrastructure/         # Settings and OpenAI gateway
├── bootstrap.py            # Dependency composition
└── main.py                 # FastAPI application
tests/                      # API and OpenAI gateway tests
```

## Troubleshooting

- **Readiness returns 503:** set `OPENAI_API_KEY` and restart.
- **Interpretation returns 503:** run `docker compose logs backend` and verify
  the key, API access, billing, model, and connectivity.
- **Browser reports CORS:** include the exact frontend origin in
  `ALLOWED_ORIGINS`.
