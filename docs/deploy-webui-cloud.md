# Web UI Cloud Deployment

This guide covers deploying the API and web UI to a cloud host. Use it together
with `docs/DEPLOY.md` for full environment configuration.

## Components

- Backend: FastAPI app from `server.py`.
- Web frontend: `apps/dsa-web`.
- Optional workers: scheduled analysis and alert monitor.
- Persistent data: the configured database and any mounted report/data
  directories.

## Build

Backend dependencies:

```bash
pip install -r requirements.txt
```

Web build:

```bash
cd apps/dsa-web
npm ci
npm run build
```

## Runtime

Start the backend:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

For a combined deployment, serve the web build through your platform's static
asset support or a reverse proxy, and route API requests to the backend service.

## Environment

At minimum configure:

- one LLM provider or channel
- `STOCK_LIST`
- optional search provider credentials
- optional notification channels
- persistent database path or external database settings

Do not store secrets in repository files. Use the host's secret manager.

## Health Checks

Use the API health endpoint and a basic page load as deployment checks. If the
web client loads but API calls fail, verify the API base URL, reverse proxy path,
CORS settings, and backend service logs.

## Rollback

Rollback should restore:

- previous container image or deploy artifact
- previous environment variables
- previous database snapshot if a migration was part of the change

Document any skipped smoke tests in the deployment record.
