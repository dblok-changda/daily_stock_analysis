# Tushare Stock List Maintenance

This project can enrich the built-in A-share stock index with Tushare data. The
index is used by autocomplete, stock-code normalization, and name-to-code
resolution.

## Prerequisites

- Set `TUSHARE_TOKEN` in your environment when fetching from Tushare.
- Keep generated index files out of ad-hoc edits unless the update is part of a
  reviewed stock-index refresh.
- Run the fetch command from the repository root.

## Fetch The Source List

```bash
python scripts/fetch_tushare_stock_list.py
```

The script reads from Tushare and writes the downloaded source list used by the
index generator. Network errors should be treated as external-provider failures;
retry later instead of committing partial data.

## Generate The Web Index

```bash
python scripts/generate_stock_index.py
```

This updates the stock index consumed by the web application. Review the diff for
unexpected market, code, or name changes before including the generated files in
a PR.

## Verification

Run the deterministic tests that cover the loader and index generation:

```bash
python -m pytest tests/test_fetch_tushare_stock_list.py tests/test_generate_index_from_csv.py tests/test_stock_index_loader.py
```

If the change affects the web autocomplete path, also run:

```bash
cd apps/dsa-web
npm run test -- stockIndexLoader searchStocks
```

## Review Checklist

- The source list was fetched with a valid `TUSHARE_TOKEN`.
- Generated files contain complete records, not error payloads.
- A-share, Hong Kong, US, JP, KR, and TW market support still loads.
- Tests pass or any network-related gap is documented in the PR.
