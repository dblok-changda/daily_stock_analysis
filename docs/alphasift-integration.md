# AlphaSift Integration

AlphaSift is an optional screening and hotspot integration. It is disabled by
default and should not change the normal analysis path unless explicitly enabled.

## Configuration

Primary switch:

```bash
ALPHASIFT_ENABLED=false
```

Optional settings are documented in `.env.example` and surfaced in Web Settings.
Do not hard-code provider paths, models, or credentials in code.

Important compatibility rule: `ALPHASIFT_ENABLED` affects only AlphaSift
screening. It must not rewrite, migrate, or clean existing `LITELLM_*`, `LLM_*`,
Agent, or Vision configuration.

## Data Paths

AlphaSift runtime data is kept under:

- `data/alphasift`
- `data/alphasift/snapshot.last_good.json`
- `data/alphasift/daily_history`
- `data/alphasift/industry_provider_cache`

These paths are runtime data, not source-of-truth configuration.

## API Surface

The web app uses AlphaSift through API routes such as:

- `/api/v1/alphasift/hotspots`
- `/api/v1/alphasift/hotspots/{topic}`
- `/api/v1/alphasift/screen/tasks`
- `/api/v1/alphasift/screen/tasks/{task_id}`

Expected error boundaries include `400`, `403`, `422`, and `424` for bad input,
disabled integration, validation errors, and missing dependency/state cases.

## Runtime Behavior

- Screening runs as a background task.
- The Screening page should be able to restore active task status after reload.
- Slow snapshots, quotes, or LLM ranking must not make the UI lose task feedback.
- LLM reranking is optional; when it times out or is unavailable, the system
  should return non-LLM ranking results with diagnostics.
- Industry/concept provider enrichment is optional and can remain disabled.

## Integration Boundaries

AlphaSift should reuse existing DSA services for stock metadata, quote access,
task status, diagnostics, and LLM configuration. Avoid adding a parallel
provider/model configuration path.

## Verification

```bash
python -m pytest tests/test_alphasift_api.py
cd apps/dsa-web && npm run test -- alphasift StockScreeningPage
```

If online screening requires external AlphaSift dependencies or provider data
that are unavailable locally, document the skipped online check and include the
deterministic test results.
