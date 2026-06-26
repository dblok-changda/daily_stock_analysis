# Real-Time Alert Center

The alert center evaluates configured market, stock, watchlist, and portfolio
rules and routes triggered alerts through the existing notification system. This
page preserves the Issue #1202 Alert Center contract, including EventMonitor and
P1 Alert API MVP behavior.

Configuration entry points:

- `AGENT_EVENT_MONITOR_ENABLED`
- `AGENT_EVENT_MONITOR_INTERVAL_MINUTES`
- `AGENT_EVENT_ALERT_RULES_JSON`

Persisted rules are managed through the Alert API and Web UI. Legacy JSON rules
remain supported for compatibility.

## Scope And Phases

- P0: documentation, storage assessment, and compatibility tests.
- P1: persisted rule contract, including `price_change_percent` and
  `data_timestamp`.
- P2/P3: API and Web rule management.
- P4: notification attempts, cooldown, and noise-boundary documentation.
- P5: route-aware notification behavior.
- P6: DecisionSignal summary linkage and portfolio/market targets.
- P7/P8: follow-up hardening and UX refinements.

## Architecture

Implementation anchors:

- `api/v1/endpoints/alerts.py`
- `api/v1/schemas/alerts.py`
- `src/storage.py`
- `src/repositories/`
- `src/services/`
- `src/services/alert_worker.py`
- `src/services/alert_service.py`
- `src/notification_noise.py`

Alert evaluation writes trigger history and notification attempts. Real
notification attempts are persisted in `alert_notifications`.

Public API routes include:

- `GET /api/v1/alerts/rules`
- `POST /api/v1/alerts/rules`
- `GET /api/v1/alerts/rules/{rule_id}`
- `PATCH /api/v1/alerts/rules/{rule_id}`
- `DELETE /api/v1/alerts/rules/{rule_id}`
- `POST /api/v1/alerts/rules/{rule_id}/test`
- `GET /api/v1/alerts/triggers`

## Rule Types

Persisted rules support:

- price threshold
- `price_change_percent`
- volume
- daily technical indicators
- `watchlist`
- `portfolio_holdings`
- `portfolio_account`
- `market` Market Light targets
- `portfolio_stop_loss`

Legacy `AGENT_EVENT_ALERT_RULES_JSON` supports only the historical basic rule
types and does not write persisted cooldown state.

Legacy JSON rule type tokens include `price_cross`, `price_change_percent`,
`volume_spike`, `sentiment_shift`, `risk_flag`, and `custom`.

## Trigger History

The worker writes `triggered`, `skipped`, `degraded`, and `failed` rows. Normal
non-triggered checks do not write history.

For DB-persisted rules, triggered rows are best-effort deduplicated by
`rule_id + target + data_source + data_timestamp`. Records without
`data_timestamp` are not deduplicated.

## Notifications And Cooldown

P4 defines notification attempts and cooldown behavior.

Triggered alerts route through `NOTIFICATION_ALERT_CHANNELS`. Per-channel
attempts are recorded under `alert_notifications`.

Cooldown uses persisted rule state for DB-backed rules. If reading persisted
cooldown state fails, the worker temporarily falls back to the in-process
fingerprint guard so a database issue does not create repeated notifications.

`notification_noise.py` remains independent. Static notification dedup and
cooldown apply to notification routing; alert business cooldown applies to alert
rules.

## Technical Indicator Rules

Technical indicators use daily-close edge triggers only. The current partial-bar
handling is a server-local-time plus `16:00` heuristic and is not a full exchange
calendar model.

Documented formulas include:

- EMA smoothing: `alpha=1/period`
- KDJ smoothing: `alpha=1/k_period`
- Example threshold: `0.015`

## Market And Portfolio Targets

P6 defines DecisionSignal, portfolio, and market-target integration.

- `watchlist` expands the current `STOCK_LIST` on each worker run.
- `portfolio_holdings` expands non-zero positions with symbol de-duplication.
- `portfolio_account` reuses portfolio risk evaluation.
- `market` accepts `cn|hk|us` and uses structured `MarketLightSnapshot` data.
- Non-trading days are skipped by the trading-day gate.
- `decision_signal_summary` can be attached to diagnostics when an active
  same-symbol DecisionSignal exists.

## GitHub Actions

The default `.github/workflows/00-daily-analysis.yml` imports the alert monitor
environment keys explicitly. Adding new repository Secrets or Variables is not
enough unless the workflow maps the key into `env:`.

## Verification

```bash
python -m pytest tests/test_alerts_docs.py tests/test_alert_api.py tests/test_alert_worker.py
```
