# Run Diagnostics P0

P0 defines the baseline diagnostics contract for analysis runs. It records the
minimum information needed to understand whether a run started, which stock or
market task it targeted, and whether it completed successfully.

## Scope

- Persist run records through `src/storage.py`.
- Keep repository access behind `src/repositories/`.
- Keep orchestration and summarization in `src/services/`.
- Store sanitized error messages instead of raw provider exceptions.

## Required Fields

Run diagnostics should include:

- run or task identifier
- stock code or market-review target
- success state
- sanitized error message when the run fails
- record counts for fetched data when available
- timestamps suitable for history and API display

## Compatibility

P0 must not change the public analysis result schema. Diagnostics are additional
metadata and should remain safe to omit for older records.

## Verification

```bash
python -m pytest tests/test_run_diagnostics_p1.py
```
