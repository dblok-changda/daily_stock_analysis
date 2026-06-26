from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_searxng_env_example_and_workflow_mapping_are_documented():
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/00-daily-analysis.yml").read_text(
        encoding="utf-8"
    )
    full_guide = (ROOT / "docs/full-guide.md").read_text(encoding="utf-8")

    assert "SEARXNG_BASE_URLS" in env_example
    assert "SEARXNG_BASE_URLS" in workflow
    assert "SearXNG" in full_guide
