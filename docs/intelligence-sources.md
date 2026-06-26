# Intelligence Sources

The analysis pipeline can combine market data, search results, social signals,
and optional intelligence services. Each source should improve context without
making the main analysis path fragile.

## Source Categories

- Market data: quotes, daily bars, fundamentals, capital flow, and index data
  from the configured data providers.
- News search: provider-backed web search such as Anspire, SerpAPI, Tavily,
  Bocha, Brave Search, MiniMax, or SearXNG.
- Social and prediction data: optional social API or Polymarket-style context
  when configured.
- Internal memory: stored analysis history, portfolio context, decision signals,
  and alert outcomes.

## Reliability Rules

- A single optional source failure must not fail the whole analysis run.
- Timeouts and missing keys should produce explicit diagnostics.
- Provider-specific fields should be normalized before they enter shared report
  or API schemas.
- Source freshness should be visible when stale data could affect analysis.

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
