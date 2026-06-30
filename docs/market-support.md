# Market Support

Daily Stock Analysis supports A-share, Hong Kong, US, Japan, Korea, and Taiwan
market symbols. Market handling is shared by the backend, web autocomplete,
stock-index loading, and data-provider routing.

## Symbol Examples

- A-share: `600519`, `000001`, `bj430047`
- Hong Kong: `hk00700`, `00700.HK`
- US: `AAPL`, `MSFT`
- Japan: `7203.T`
- Korea: `005930.KS`
- Taiwan: `2330.TW`

## Compatibility Rules

- Do not hard-code one market's symbol rules into shared code paths.
- Preserve old accepted formats when adding normalized formats.
- Keep display names separate from provider routing symbols.
- Prefer additive schema changes for API and web compatibility.

## Verification

Run market and symbol tests when changing routing, normalization, or index data:

```bash
python -m pytest tests/test_stock_code_utils.py tests/test_jp_kr_market_support.py tests/test_tw_market_support.py tests/test_yfinance_hk_indices.py tests/test_yfinance_us_indices.py
```

For web autocomplete changes, also run the stock-index loader and search tests in
`apps/dsa-web`.

Rollback: remove `jp/kr/tw` market detection, trading-calendar registration, YFinance
route expansion, Web/API type allowance, and the related `scripts/stock_index_seeds/`
index seed files, then remove the capability statements from this document.

## Taiwan Suffix-Only MVP (Issue #1772, Refs #1772)

The current code supports manual entry of Taiwan Yahoo Finance suffix symbols through
the existing single-stock analysis, history persistence, and basic report display flow.
TWSE listings use the `.TW` suffix, and TPEX OTC listings use the `.TWO` suffix. Both
are folded into the same `tw` market tag.

Supported examples:

- TWSE: `2330.TW`, `0050.TW`
- TPEX / OTC: `6488.TWO`, `5483.TWO`
- Base numeric codes are usually 4-6 digits. Common stocks often use 4 digits, while
  ETFs and other products can use 6 digits, such as `00878.TW` and `006208.TW`.

Boundaries:

- Strict suffix-only handling: bare codes such as `2330` or `00878` are not interpreted
  as Taiwan stocks. `detect_market` / `get_market_for_stock` only return `tw` when the
  explicit `.TW` or `.TWO` suffix is present. This release intentionally does not add
  Taiwan stock index or seed-code resolution.
- Taiwan daily and basic real-time or near-real-time stock data currently use only the
  `YfinanceFetcher`; it does not try A-share-only providers such as AkShare, Tushare,
  QFinance, Pytdx, or Baostock.
- Fundamental reuse follows the existing lightweight offshore YFinance path. A-share-only
  capital-flow, dragon-tiger, and sector capabilities remain `not_supported`.
- Report prompts include Taiwan market language for New Taiwan dollar, the three major
  institutional investors, and TWSE/TPEX +/-10% price limits, avoiding A-share-specific
  concepts such as northbound capital flow or dragon-tiger lists.
- The `tw` trading calendar maps to `XTAI` / `Asia/Taipei`. TWSE trades continuously
  from 09:00 to 13:30 without a lunch break. Closing-auction parts are not modeled,
  consistent with the `jp/kr` MVP calendar behavior.
- Major index support exposes weighted index `^TWII` and OTC index `^TWOII`.

Non-goals:

- No guarantee of real-time quotes; Yahoo Finance data can be delayed or sparse.
- No complete fundamentals, industry/sector, market breadth, advancer/decliner, or
  Taiwan market-review coverage.
- Taiwan stock index/seed-code resolution, Web autocomplete, and alert market release are
  follow-up work rather than part of this MVP.
- Portfolio TWD FX, cost, and market-value completeness are follow-up work.
