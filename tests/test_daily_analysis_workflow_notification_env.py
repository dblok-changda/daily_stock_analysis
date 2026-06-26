from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT_DIR / ".github/workflows/00-daily-analysis.yml"
NOTIFICATIONS_DOC_PATH = ROOT_DIR / "docs/notifications.md"

P0_ACTIONS_ENV_KEYS = (
    "WECHAT_WEBHOOK_URL",
    "FEISHU_WEBHOOK_URL",
    "TELEGRAM_BOT_TOKEN",
    "DISCORD_WEBHOOK_URL",
    "SLACK_WEBHOOK_URL",
)

P3_ROUTE_ENV_KEYS = (
    "NOTIFICATION_REPORT_CHANNELS",
    "NOTIFICATION_ALERT_CHANNELS",
    "NOTIFICATION_SYSTEM_ERROR_CHANNELS",
)

P4_NOISE_ACTIONS_ENV_KEYS = (
    "NOTIFICATION_DEDUP_TTL_SECONDS",
    "NOTIFICATION_COOLDOWN_SECONDS",
    "NOTIFICATION_QUIET_HOURS",
    "NOTIFICATION_TIMEZONE",
    "NOTIFICATION_MIN_SEVERITY",
    "NOTIFICATION_DAILY_DIGEST_ENABLED",
)

P6_CHANNEL_ACTIONS_ENV_KEYS = ("NTFY_URL", "GOTIFY_URL")


def _get_analyze_env() -> dict[str, object]:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["analyze"]["steps"]
    analyze_step = next(
        (step for step in steps if step.get("name") == "Run stock analysis"),
        None,
    )
    assert analyze_step is not None
    return analyze_step.get("env", {})


def test_daily_analysis_maps_p0_notification_env_keys() -> None:
    env = _get_analyze_env()
    for key in P0_ACTIONS_ENV_KEYS:
        assert key in env


def test_daily_analysis_maps_p3_notification_route_env_keys() -> None:
    env = _get_analyze_env()
    for key in P3_ROUTE_ENV_KEYS:
        assert key in env


def test_daily_analysis_maps_p4_notification_noise_env_keys() -> None:
    env = _get_analyze_env()
    for key in P4_NOISE_ACTIONS_ENV_KEYS:
        assert key in env


def test_daily_analysis_maps_p6_channel_env_keys() -> None:
    env = _get_analyze_env()
    for key in P6_CHANNEL_ACTIONS_ENV_KEYS:
        assert key in env


def test_daily_analysis_feishu_status_accepts_webhook_or_app_bot_triad() -> None:
    env = _get_analyze_env()
    for key in (
        "FEISHU_WEBHOOK_URL",
        "FEISHU_APP_ID",
        "FEISHU_APP_SECRET",
        "FEISHU_CHAT_ID",
    ):
        assert key in env


def test_notifications_doc_table_mentions_workflow_mapping() -> None:
    doc = NOTIFICATIONS_DOC_PATH.read_text(encoding="utf-8")
    for key in ("WECHAT_WEBHOOK_URL", "FEISHU_WEBHOOK_URL", "NTFY_URL", "GOTIFY_URL"):
        assert key in doc
    assert "<!-- notification-actions-env-table:start -->" in doc
    assert "<!-- notification-actions-env-table:end -->" in doc
