# Discord Bot Configuration

The Discord integration supports command handling, interaction responses, and
optional report delivery.

## Required Settings

Configure the values used by the Discord platform implementation:

- `DISCORD_BOT_TOKEN`
- `DISCORD_APPLICATION_ID`
- `DISCORD_PUBLIC_KEY`
- Channel IDs used for command routing or report delivery, when enabled.

Keep secrets in `.env`, deployment secrets, or the hosting platform's secret
store. Do not commit real Discord credentials.

## Behavior

- Commands should be parsed by `bot/commands/*` and dispatched through the shared
  bot handler.
- Long-running analysis should return a progress or queued response instead of
  blocking the interaction timeout.
- Errors returned to Discord users should be concise and in English.
- Webhook/report delivery should reuse the notification sender where possible.

## Verification

Run:

```bash
python -m pytest tests/test_discord_platform.py tests/test_bot_dispatcher_async.py
```

For interaction changes, also perform a manual Discord smoke test when a test app
is available.
