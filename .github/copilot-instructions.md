# Copilot Instructions

Canonical source: `AGENTS.md` is the source of truth for repository
collaboration rules. If this file conflicts with `AGENTS.md`, follow
`AGENTS.md`. `CLAUDE.md` is maintained as the Claude-compatible pointer to the
same rules.

Repository-specific skill documents live in `.claude/skills/`.

## Scope Boundaries

- Backend: `src/`, `data_provider/`, `api/`, `bot/`
- Web frontend: `apps/dsa-web/`
- Desktop: `apps/dsa-desktop/`
- Deployment, scripts, workflows, Docker: `scripts/`, `.github/workflows/`,
  `docker/`

## Change Discipline

- Do not commit, tag, or push unless explicitly asked.
- Prefer existing modules, configuration paths, scripts, and tests.
- Keep changes scoped to the requested behavior.
- Do not hard-code secrets, accounts, local paths, models, ports, or
  environment-specific logic.
- Update `.env.example` and relevant docs when adding configuration.
- Update `docs/CHANGELOG.md` for user-visible CLI/API/Web/Desktop/workflow,
  report, notification, or deployment changes.

## PR Titles

Recommended title format: `<type>: <summary>`.

Preferred types: `fix`, `feat`, `refactor`, `docs`, `chore`, `test`, `ci`.
Avoid tool/source prefixes such as `[codex]`, `codex`, `autocode`, or `copilot`.

## Verification

- Python/backend changes: prefer `./scripts/ci_gate.sh`; minimum is
  `python -m py_compile <changed_python_files>`.
- Web changes: `cd apps/dsa-web && npm ci && npm run lint && npm run build`.
- Desktop changes: build the web app first, then `cd apps/dsa-desktop &&
  npm run build`.
- AI collaboration asset changes: `python scripts/check_ai_assets.py`.

## Review Expectations

For fixes, explain the original problem, root cause, fix, and regression risk.
Do not use broad fallbacks or silent `None`/`False`/empty returns to hide unclear
contracts.

When addressing review feedback, re-check all paths affected by the same
business meaning: runtime, API/Web, CLI, diagnostics, workflow, docs, tests, and
user-visible output.

## Documentation

Keep README focused on project positioning, core capabilities, quick start, and
main entry points. Put detailed module behavior, troubleshooting, configuration,
and contracts in `docs/*.md`.
