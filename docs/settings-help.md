# Settings Help

The Settings page exposes environment-backed configuration through grouped,
validated fields. Help text should explain what a setting does without changing
runtime behavior or duplicating implementation details from code.

## Principles

- Keep labels and descriptions in English.
- Keep secret values masked.
- Use existing registry metadata from `src/core/config_registry.py`.
- Do not create a parallel settings schema in documentation.
- When adding a setting, update `.env.example`, registry metadata, tests, and the
  relevant docs.

## Main Categories

- AI model and LLM channels.
- Data sources and search providers.
- Report and notification output.
- Alert monitor and event rules.
- Web/API authentication and runtime behavior.

## LLM Channels

The channel editor maps `LLM_CHANNELS` and `LLM_<CHANNEL>_*` fields. Prefer
Channels for new multi-provider setups. YAML mode is for advanced LiteLLM routing
and has higher priority than Channels.

## Notifications

Notification settings include channel credentials, route keys, and noise-control
keys. Minimal channel keys enable channels; advanced keys only modify already
enabled channels. See `docs/notifications.md`.

## Validation

Validation should return actionable English messages with:

- key name
- expected shape
- actual issue
- whether the field is sensitive

Do not silently drop invalid values unless the existing runtime contract already
defines a safe fallback.

## Verification

```bash
python -m pytest tests/test_config_registry.py tests/test_system_config_service.py tests/test_system_config_api.py
cd apps/dsa-web && npm run test -- systemConfig
```
