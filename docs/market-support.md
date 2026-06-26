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
