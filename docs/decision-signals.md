# DecisionSignal Topic

This page closes the #1390 P7 documentation scope for `DecisionSignal`. A
DecisionSignal is a structured index over analysis, Agent, alert, and portfolio
risk advice. It does not replace Markdown reports, `operation_advice`,
three-state `decision_type`, alert rules, or any real trading system.

## Boundaries

- `DecisionSignal` records advice, evidence summary, risk, watch conditions,
  lifecycle, and source.
- It never places orders or changes a portfolio.
- Existing `decision_type=buy|hold|sell` behavior remains compatible.
- No `DECISION_SIGNAL_*` runtime configuration is introduced in P7.

## Schema

The live API schema is defined in `api/v1/schemas/decision_signals.py`.
Important public models include:

- `DecisionSignalCreateRequest`
- `DecisionSignalItem`
- `DecisionSignalOutcomeItem`
- `DecisionSignalFeedbackRequest`
- `PortfolioDecisionSignalRiskBlock`

Core fields include source identity, market, stock code, action, horizon,
market phase, trigger source, status, expiry, entry range, `stop_loss`,
`target_price`, `invalidation`, `watch_conditions`, `reason`, `risk_summary`,
and `catalyst_summary`.

## Service And Storage

`src/services/decision_signal_service.py` is the lifecycle entry point.
`src/repositories/decision_signal_repo.py` owns DB access. Storage tables are
defined in `src/storage.py`:

- `decision_signals`
- `decision_signal_feedback`
- `decision_signal_outcomes`

Writes and status updates sanitize text with:

- `sanitize_decision_signal_text()`
- `sanitize_decision_signal_payload()`

## API

The public endpoints are implemented in
`api/v1/endpoints/decision_signals.py` and described in
`docs/architecture/api_spec.json`.

Important paths:

- `POST /api/v1/decision-signals`
- `GET /api/v1/decision-signals`
- `GET /api/v1/decision-signals/latest/{stock_code}`
- `GET /api/v1/decision-signals/{signal_id}`
- `PATCH /api/v1/decision-signals/{signal_id}/status`
- `POST /api/v1/decision-signals/outcomes/run`
- `GET /api/v1/decision-signals/outcomes`
- `GET /api/v1/decision-signals/outcomes/stats`
- `GET /api/v1/decision-signals/{signal_id}/outcomes`
- `GET /api/v1/decision-signals/{signal_id}/feedback`
- `PUT /api/v1/decision-signals/{signal_id}/feedback`

## Integrations

This section covers analysis history, Alert triggers, GET /api/v1/portfolio/risk,
and rollback-facing integration behavior.

- Analysis history extraction stores best-effort signals after history is saved.
- Alert triggers link the latest active same-symbol signal when available and
  write a low-sensitive `decision_signal_summary` into diagnostics.
- `GET /api/v1/portfolio/risk` exposes `decision_signal_risk` for current
  holdings and fails open when signal lookup is unavailable.
- Notifications may render public excerpts through
  `src/services/decision_signal_summary.py`.

## Feedback And Outcomes

P5 stores user feedback and forward outcome evaluation in sidecar tables instead
of expanding the main `decision_signals` table. Outcome rows are idempotent by
`(signal_id, horizon, engine_version)`.

## Compatibility And Rollback

Existing signal, feedback, and outcome rows remain compatible. Rolling back P7
stops new signal extraction and writes, but report saving, alert triggering,
notification sending, and portfolio risk main flow continue through their
existing paths. Historical rows are not deleted automatically; any cleanup must
be planned separately.

## Verification

```bash
python -m pytest tests/test_decision_signal_docs.py tests/test_decision_signal_api.py tests/test_decision_signal_service.py tests/test_decision_signal_repo.py
```
