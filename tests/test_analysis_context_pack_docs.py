from pathlib import Path


DOC_PATH = Path("docs/analysis-context-pack.md")
FULL_GUIDE_PATH = Path("docs/full-guide.md")


def _read_doc() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def test_analysis_context_pack_doc_keeps_phase_scope():
    doc = _read_doc()

    for token in ("P0", "P1", "P2", "P3", "P4", "P5", "P6"):
        assert token in doc

    assert "Later phases must not be described as part of P1" in doc


def test_analysis_context_pack_doc_lists_core_blocks():
    doc = _read_doc()

    for token in (
        "`quote`",
        "`daily_bars`",
        "`technical`",
        "`fundamentals`",
        "`news`",
        "`portfolio`",
        "`capital_flow`",
        "`market_context`",
    ):
        assert token in doc


def test_analysis_context_pack_doc_records_status_and_redaction_contract():
    doc = _read_doc()

    for token in (
        "`ok`",
        "`missing`",
        "`not_supported`",
        "`fetch_failed`",
        "API keys",
        "bearer tokens",
        "cookies",
        "webhook URLs",
        "Full `news.content` bodies",
    ):
        assert token in doc


def test_analysis_context_pack_doc_records_data_quality_and_visibility():
    doc = _read_doc()

    for token in (
        "`overall_score`",
        "`level`",
        "`block_scores`",
        "`limitations`",
        "`analysis_context_pack_overview`",
        "`analysis_context_pack_summary`",
        "`trend_result`",
    ):
        assert token in doc


def test_full_guide_still_links_analysis_context_pack():
    full_guide = FULL_GUIDE_PATH.read_text(encoding="utf-8")

    assert "AnalysisContextPack" in full_guide
