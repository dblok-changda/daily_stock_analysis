# Run Diagnostics P1

P1 stores component-level diagnostics for analysis data sources. The goal is to
show which inputs were available without making optional source failures fatal.

## Component Status

Components can report:

- `success`: data was fetched and accepted.
- `failed`: the component failed and produced a sanitized error.
- `skipped`: the component was intentionally not used.
- `missing`: no data was available.

Typical components include quote, historical bars, technical data, fundamentals,
news, market context, and portfolio context.

## Error Handling

Diagnostics must sanitize provider errors before storage and API exposure. Keep
raw exceptions in logs only when safe and useful for operators.

## Verification

```bash
python -m pytest tests/test_run_diagnostics_p1.py
```
