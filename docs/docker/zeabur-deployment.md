# Zeabur Deployment

This guide describes a Docker-based Zeabur deployment for Daily Stock Analysis.

## Prerequisites

- A Zeabur project.
- Repository access for this project.
- Required LLM, data-source, search, and notification environment variables.
- Persistent storage for database and generated artifacts if the deployment must
  retain history.

## Docker Image

Use the repository Dockerfile or the published image configured for this project.
Keep runtime configuration in Zeabur environment variables rather than editing
image files.

## Environment

Configure at least:

- `STOCK_LIST`
- one LLM provider or channel
- optional search provider keys
- optional notification channel keys
- database and persistence settings

For notification behavior, see `docs/notifications.md`. For LLM channels, see
`docs/llm-providers.md`.

## Startup

The service should start the FastAPI backend. Scheduled jobs and alert workers
depend on the environment flags you enable.

## Verification

- Open the web UI.
- Check the API health endpoint.
- Run a dry-run analysis if credentials are available.
- Confirm logs are in English and do not print secrets.

## Rollback

Rollback to the previous image or deployment revision and restore the previous
environment variable set. If persistent data changed, restore from the matching
backup before restarting the old revision.
