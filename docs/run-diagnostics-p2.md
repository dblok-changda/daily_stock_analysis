# Run Diagnostics P2

P2 adds trace-oriented component summaries so the UI and API can explain how an
analysis result was produced.

## Contract

Each diagnostic event should keep:

- `trace_id`
- component name such as `realtime_quote` or `news`
- operation name such as `get_realtime_quote`
- duration in milliseconds when available
- status and sanitized error details
- record count or payload summary when available

The summary should remain deterministic even when a component is absent. Missing
components should not cause summary generation to fail.

## Verification

```bash
python -m pytest tests/test_run_diagnostics_p2.py
```
