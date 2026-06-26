# DingTalk Bot Configuration

The DingTalk integration lets the bot receive commands and send analysis
responses through DingTalk.

## Configuration

Set the DingTalk-related variables in `.env` or your deployment secret store.
Use the variable names already present in `.env.example`; do not hard-code tokens
in code or workflow files.

Typical settings include:

- DingTalk app credentials or webhook credentials.
- Bot command routing options.
- Optional notification settings shared with the main notification system.

## Runtime Notes

- Keep command parsing in the bot layer and analysis execution in existing
  services.
- A DingTalk delivery failure should be reported through diagnostics without
  crashing unrelated analysis work.
- Return English error messages with enough context for the operator to fix the
  missing credential, invalid signature, or network failure.

## Verification

Run the DingTalk stream and dispatcher tests after changes:

```bash
python -m pytest tests/test_bot_dispatcher_async.py tests/test_feishu_stream.py
```

If the change requires a real DingTalk tenant, document the manual verification
or the reason it was skipped.
