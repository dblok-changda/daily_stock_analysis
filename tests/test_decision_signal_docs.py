from pathlib import Path


DOC_PATH = Path("docs/decision-signals.md")
API_SPEC_PATH = Path("docs/architecture/api_spec.json")


def _read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_decision_signal_doc_lists_schema_and_storage_contracts():
    doc = _read_doc()

    for token in (
        "DecisionSignal",
        "DecisionSignalCreateRequest",
        "DecisionSignalItem",
        "DecisionSignalOutcomeItem",
        "DecisionSignalFeedbackRequest",
        "PortfolioDecisionSignalRiskBlock",
        "`decision_signals`",
        "`decision_signal_feedback`",
        "`decision_signal_outcomes`",
    ):
        assert token in doc


def test_decision_signal_doc_lists_service_and_sanitizer_paths():
    doc = _read_doc()

    for token in (
        "`api/v1/schemas/decision_signals.py`",
        "`src/services/decision_signal_service.py`",
        "`src/repositories/decision_signal_repo.py`",
        "`src/storage.py`",
        "`sanitize_decision_signal_text()`",
        "`sanitize_decision_signal_payload()`",
    ):
        assert token in doc


def test_decision_signal_doc_lists_public_api_paths():
    doc = _read_doc()

    for token in (
        "/api/v1/decision-signals",
        "/api/v1/decision-signals/latest/{stock_code}",
        "/api/v1/decision-signals/outcomes/run",
        "/api/v1/decision-signals/{signal_id}/feedback",
    ):
        assert token in doc


def test_decision_signal_doc_lists_integration_and_rollback_scope():
    doc = _read_doc()

    for token in (
        "analysis history",
        "Alert triggers",
        "GET /api/v1/portfolio/risk",
        "`decision_signal_risk`",
        "`src/services/decision_signal_summary.py`",
        "Compatibility And Rollback",
    ):
        assert token in doc


def test_decision_signal_api_spec_keeps_public_paths():
    api_spec = API_SPEC_PATH.read_text(encoding="utf-8")

    for token in (
        "/api/v1/decision-signals",
        "/api/v1/decision-signals/latest/{stock_code}",
        "/api/v1/decision-signals/outcomes/run",
        "/api/v1/decision-signals/{signal_id}/feedback",
    ):
        assert token in api_spec
