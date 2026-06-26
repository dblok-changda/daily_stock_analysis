# Strategy Definitions

This directory contains YAML strategy presets used by the analysis pipeline.
Each strategy describes market conditions, signal hints, risk controls, and
prompt-facing context for a style of trading or screening.

## Editing Rules

- Keep YAML valid and human-readable.
- Do not add secrets, account data, or environment-specific paths.
- Preserve existing field names unless the strategy loader and tests are updated
  in the same change.
- Prefer small, focused edits to strategy wording or thresholds.

## Validation

Run strategy and analysis tests after changing YAML files:

```bash
python -m pytest tests/test_market_strategy.py tests/test_stock_analyzer_bias.py
```

If a strategy change is intended to affect report wording, include before/after
report evidence in the PR description.
