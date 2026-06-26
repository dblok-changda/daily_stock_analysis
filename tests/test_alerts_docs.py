from pathlib import Path


DOC_PATH = Path("docs/alerts.md")


def _read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_alerts_doc_keeps_core_contract_anchors():
    doc = _read_doc()

    for token in (
        "Issue #1202",
        "AGENT_EVENT_MONITOR_ENABLED",
        "AGENT_EVENT_MONITOR_INTERVAL_MINUTES",
        "AGENT_EVENT_ALERT_RULES_JSON",
        "EventMonitor",
        "P1 Alert API MVP",
    ):
        assert token in doc


def test_alerts_doc_lists_runtime_paths_and_api_routes():
    doc = _read_doc()

    for token in (
        "`api/v1/endpoints/alerts.py`",
        "`api/v1/schemas/alerts.py`",
        "`src/storage.py`",
        "`src/repositories/`",
        "`src/services/`",
        "GET /api/v1/alerts/rules",
        "POST /api/v1/alerts/rules",
        "PATCH /api/v1/alerts/rules/{rule_id}",
        "DELETE /api/v1/alerts/rules/{rule_id}",
    ):
        assert token in doc


def test_alerts_doc_defines_rule_types_and_trigger_fields():
    doc = _read_doc()

    for token in (
        "price_cross",
        "price_change_percent",
        "volume_spike",
        "sentiment_shift",
        "risk_flag",
        "custom",
        "data_timestamp",
        "triggered",
        "skipped",
        "degraded",
        "failed",
    ):
        assert token in doc


def test_alerts_doc_defines_p4_notification_and_cooldown_scope():
    doc = _read_doc()

    for token in (
        "P4",
        "`NOTIFICATION_ALERT_CHANNELS`",
        "`alert_notifications`",
        "`notification_noise.py`",
        "cooldown",
    ):
        assert token in doc


def test_alerts_doc_defines_technical_indicator_scope():
    doc = _read_doc()

    for token in ("16:00", "alpha=1/period", "alpha=1/k_period", "0.015"):
        assert token in doc


def test_alerts_doc_defines_p6_market_and_decision_signal_scope():
    doc = _read_doc()

    for token in (
        "P6",
        "`watchlist`",
        "`portfolio_holdings`",
        "`portfolio_account`",
        "`market`",
        "`decision_signal_summary`",
        "DecisionSignal",
    ):
        assert token in doc


def test_alerts_doc_mentions_workflow_mapping_and_verification():
    doc = _read_doc()

    for token in (
        "`.github/workflows/00-daily-analysis.yml`",
        "env:",
        "tests/test_alerts_docs.py",
        "tests/test_alert_api.py",
        "tests/test_alert_worker.py",
    ):
        assert token in doc
