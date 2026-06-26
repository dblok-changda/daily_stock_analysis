# Feishu Bot Configuration

The Feishu integration supports stream-based bot commands and report delivery.

## Configuration

Use the Feishu variables from `.env.example` and your deployment environment.
Common values include app credentials, verification tokens, encryption keys, and
stream-mode options.

Do not duplicate Feishu credentials in code, docs examples, or workflow files.

## Runtime Rules

- Feishu event parsing belongs in the platform adapter.
- Command behavior should reuse the existing bot command classes.
- Analysis, market review, and history lookup should call the shared services
  instead of platform-specific implementations.
- Missing credentials and signature failures should produce English diagnostics.

## Verification

Run:

```bash
python -m pytest tests/test_feishu_stream.py tests/test_bot_dispatcher_async.py
```

If real Feishu stream verification is skipped, document that gap in the PR.
