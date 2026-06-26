# OpenClaw Skill Integration

This document describes the product-facing OpenClaw skill integration. It is not
the repository's AI collaboration rule source; repository collaboration rules
live in `AGENTS.md`.

## Purpose

OpenClaw integrations should expose stock-analysis capabilities through a stable
skill surface while reusing the existing backend services, schemas, and
configuration. New skill behavior should not create a parallel implementation of
analysis, notification, or data-provider logic.

## Integration Rules

- Route analysis requests through existing service boundaries.
- Reuse existing API schemas when returning reports, diagnostics, and task
  status.
- Keep provider keys and runtime configuration in environment variables or the
  existing settings service.
- Surface errors in English and include actionable diagnostics.
- Avoid hidden fallbacks that make failed provider configuration look
  successful.

## Verification

When changing OpenClaw-facing behavior, run the affected backend tests and any
API contract tests for the endpoints used by the skill.

```bash
python -m pytest tests/test_analysis_api_contract.py tests/test_task_service.py
```

Document any unverified external OpenClaw checks in the PR.
