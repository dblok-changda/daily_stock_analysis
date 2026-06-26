# Daily Stock Analysis Skill

Use this skill when working on Daily Stock Analysis features, fixes, reports,
data providers, notifications, or deployment behavior.

## Project Shape

The project fetches stock data, enriches it with technical analysis and news,
runs LLM analysis, renders reports, and optionally sends notifications.

Main entry points:

- `main.py`: CLI and scheduled analysis entry.
- `server.py`: FastAPI entry.
- `apps/dsa-web/`: Web frontend.
- `apps/dsa-desktop/`: Electron desktop shell.

## Development Rules

1. Read the relevant existing implementation before editing.
2. Reuse existing service, repository, configuration, and test patterns.
3. Keep changes scoped to the requested behavior.
4. Update `.env.example`, docs, and `docs/CHANGELOG.md` for user-visible or
   configuration changes.

## Validation

- Backend: `./scripts/ci_gate.sh` or targeted `python -m pytest ...`.
- Web: `cd apps/dsa-web && npm run lint && npm run build`.
- Desktop: build the web app first, then `cd apps/dsa-desktop && npm run build`.
- AI governance assets: `python scripts/check_ai_assets.py`.
