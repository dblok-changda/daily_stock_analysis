# Intelligence Sources

The analysis pipeline can combine market data, search results, social signals,
and optional intelligence services. Each source should improve context without
making the main analysis path fragile.

## Source Categories

- Market data: quotes, daily bars, fundamentals, capital flow, and index data
  from the configured data providers.
- News search: provider-backed web search such as Anspire, SerpAPI, Tavily,
  Bocha, Brave Search, MiniMax, or SearXNG.
- Configured intelligence feeds: built-in RSS/Atom HTTP(S) sources, NewsNow HTTP JSON
  sources, and queryable RSS/Atom/NewsNow templates. Built-in defaults cover common
  finance-news sources, and custom configured sources can be tested, enabled, disabled,
  or created from templates.
- Feed ingestion state: source configuration, enabled state, scope, and last fetch status
  are persisted. Fetched items are stored in `intelligence_items` with title, summary,
  URL, source, publish time, fetch time, market, and scope.
- Feed de-duplication and scope: URL-backed items de-duplicate by URL, while URL-less
  items use `no-url:intel:<hash>`. Supported scopes are `symbol`, `market`, and `sector`,
  with `cn`, `hk`, `us`, `jp`, `kr`, `tw`, and `global` market tags.
- Social and prediction data: optional social API or Polymarket-style context
  when configured.
- Internal memory: stored analysis history, portfolio context, decision signals,
  and alert outcomes.

## Reliability Rules

- A single optional source failure must not fail the whole analysis run.
- Feed batch fetching is fail-open: one source failure must not block other sources or the
  main analysis path.
- Timeouts and missing keys should produce explicit diagnostics.
- Provider-specific fields should be normalized before they enter shared report
  or API schemas.
- Source freshness should be visible when stale data could affect analysis.
- Retention cleanup should keep the intelligence item pool bounded.

## Configuration

Configure provider keys in `.env` or the deployment secret store. Keep provider
defaults conservative and document any new variable in `.env.example`,
`docs/full-guide.md`, and the relevant integration guide.

## Verification

Use deterministic tests first:

```bash
python -m pytest -m "not network"
```

Run provider-specific network tests only when credentials and network access are
available. Document skipped online checks in the PR.
