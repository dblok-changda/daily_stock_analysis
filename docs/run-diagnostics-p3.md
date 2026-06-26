# Run Diagnostics P3

P3 exposes diagnostics through API and UI-facing history paths.

## API Surface

The diagnostics data is returned with analysis history and task detail payloads
where available. Consumers should treat diagnostics as optional metadata.

Relevant paths include analysis history, market-review history, task status, and
completed run detail views.

## UI Rules

- Show component status without blocking the main report.
- Prefer concise English messages.
- Hide raw provider stack traces.
- Preserve timestamps and trace identifiers for operator debugging.

## Backward Compatibility

Older records may not include diagnostics. Clients must handle missing
diagnostics gracefully.

## Verification

```bash
python -m pytest tests/test_run_diagnostics_p1.py tests/test_run_diagnostics_p2.py
```
