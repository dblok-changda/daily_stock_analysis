# AnalysisContextPack

`AnalysisContextPack` is the low-sensitivity context summary shared by regular
analysis, Agent analysis, history, alerts, portfolio views, and notifications.
It exists to make data availability explicit without exposing raw payloads,
secrets, tokens, webhooks, or long news bodies.

## Phase Scope

The implementation is tracked across P0/P1 through P6:

- P0: define pack contract and compatibility boundaries.
- P1: time and status semantics for existing data blocks.
- P2: prompt section formatting.
- P3: low-sensitivity summary consumption.
- P4: history, API, and Web visibility.
- P5: data-quality scoring and model-readable limitations.
- P6: reuse across alerts, portfolio, history, backtesting, and notifications.

Later phases must not be described as part of P1. P1 only records time/status
semantics and redaction rules.

## Blocks

The fixed core blocks are:

- `quote`
- `daily_bars`
- `technical`
- `fundamentals`
- `news`
- `portfolio`

Auxiliary context can include `capital_flow` and `market_context`.

## Status Semantics

Block status should distinguish usable data from absent or degraded data without
inventing confidence:

- `ok`: usable data exists.
- `missing`: expected data is absent.
- `not_supported`: the source or market does not support the block.
- `fetch_failed`: this run explicitly failed to fetch the block.

Realtime quote timestamps should preserve the difference between system fetch
time and provider time. Do not fabricate freshness when provider timestamps are
missing.

## Redaction Contract

The pack summary must not expose:

- API keys, bearer tokens, cookies, webhook URLs, or private headers.
- Full `news.content` bodies.
- Raw trend, chip, or fundamentals payloads.
- Sensitive portfolio details beyond the low-sensitivity summary.

The LLM prompt section should include only subject, pack version, block status,
source, warnings, missing reason, news result count, data-quality score, and
limitations.

## Data Quality

P5 adds `DataQuality` fields:

- `overall_score`
- `level`
- `block_scores`
- `limitations`
- existing `warnings` and `metadata`

Scoring uses the six fixed core blocks and does not re-normalize missing
auxiliary blocks away. Missing auxiliary data constrains only the relevant
analysis section and must not be interpreted as bullish or bearish.

## Visibility

The Web UI, history, alerts, and notifications consume only the public
`analysis_context_pack_overview`. They do not expose the full pack,
`analysis_context_pack_summary`, `items.value`, raw news content, `trend_result`,
chip details, or fundamentals raw payloads.

## Verification

```bash
python -m pytest tests/test_analysis_context_pack_docs.py tests/test_analysis_context_pack_schema.py tests/test_analysis_context_pack_prompt.py
```
