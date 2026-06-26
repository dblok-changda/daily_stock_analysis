# LLM Provider Configuration Guide

This guide explains how to choose an LLM configuration style, how Web Settings
maps provider presets to `.env` / GitHub Actions, and how to diagnose common
provider errors.

## Configuration Layers

| Layer | Best for | Main keys | Notes |
| --- | --- | --- | --- |
| Legacy minimal | Quick local setup with one model | `LITELLM_MODEL` plus the matching provider key | Fewest variables; not ideal for complex fallback. |
| Channels | Multiple providers, keys, or fallback | `LLM_CHANNELS` plus `LLM_<CHANNEL>_*` | Recommended default; Web Settings saves this layer. |
| YAML | Expert LiteLLM routing, balancing, or enterprise gateways | `LITELLM_CONFIG` / `LITELLM_CONFIG_YAML` | Highest priority. When valid, Channels and legacy config do not participate in that request. |

Priority is unchanged:

```text
LITELLM_CONFIG / LITELLM_CONFIG_YAML > LLM_CHANNELS > legacy provider keys
```

This guide documents configuration only. It does not migrate, clear, or silently
rewrite old variables.

## Generation Backend

`GENERATION_BACKEND` is the outer runtime backend selector. Supported values are
`litellm` and `codex_cli`.

`codex_cli` is a local CLI backend, not a LiteLLM provider. Do not configure
`LITELLM_MODEL=codex_cli/...`.

`GENERATION_FALLBACK_BACKEND=` disables backend-level fallback in local `.env`.
When unset, fallback defaults to `litellm`. The default GitHub Actions workflow
uses `litellm` when the variable is not configured.

Agent tool-calling still uses LiteLLM. Web Settings exposes
`AGENT_GENERATION_BACKEND=auto|litellm`; manually setting `codex_cli` for Agent
tool-calling returns an unsupported-tool-calling diagnostic.

## Channel Examples

DeepSeek:

```bash
LLM_CHANNELS=deepseek
LLM_DEEPSEEK_PROTOCOL=deepseek
LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_DEEPSEEK_API_KEY=sk-xxx
LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro
LITELLM_MODEL=deepseek/deepseek-v4-flash
```

OpenAI-compatible proxy:

```bash
LLM_CHANNELS=my_proxy
LLM_MY_PROXY_PROTOCOL=openai
LLM_MY_PROXY_BASE_URL=https://your-proxy.example.com/v1
LLM_MY_PROXY_API_KEY=sk-xxx
LLM_MY_PROXY_MODELS=gpt-5.5,claude-sonnet-4-6
LITELLM_MODEL=openai/gpt-5.5
```

OpenAI-compatible Base URLs should point to the provider's compatible API root.
Do not append `/chat/completions` unless the provider specifically documents that
as the base path.

Ollama is intended for local, Docker, or self-hosted runner environments that can
reach the Ollama service:

```bash
LLM_CHANNELS=ollama
LLM_OLLAMA_PROTOCOL=ollama
LLM_OLLAMA_BASE_URL=http://127.0.0.1:11434
LLM_OLLAMA_MODELS=qwen3:8b,llama3.2
LITELLM_MODEL=ollama/qwen3:8b
```

GitHub-hosted runners usually do not have a local Ollama service.

## Provider Presets

Common preset channels include:

- `anspire`
- `aihubmix`
- `openai`
- `deepseek`
- `gemini`
- `anthropic`
- `moonshot`
- `dashscope`
- `zhipu`
- `minimax`
- `volcengine`
- `siliconflow`
- `openrouter`
- `ollama`

The default workflow explicitly maps common channels such as `primary`,
`secondary`, `aihubmix`, `anspire`, `deepseek`, `dashscope`, `zhipu`,
`moonshot`, `minimax`, `volcengine`, `siliconflow`, `openrouter`, `gemini`,
`anthropic`, `openai`, and `ollama`. Channels not listed in the workflow, such as
custom `mimo`, require corresponding `LLM_<CHANNEL>_*` env mappings in the
workflow. Local `.env`, Docker, and self-hosted scripts are not limited by that
default workflow mapping.

## GitHub Actions Secrets And Variables

| Key | Recommended storage | Notes |
| --- | --- | --- |
| `LLM_CHANNELS` | Variable or Secret | Comma-separated channel names. |
| `LLM_<CHANNEL>_PROTOCOL` | Variable or Secret | Usually `openai`, `deepseek`, `gemini`, `anthropic`, `vertex_ai`, or `ollama`. |
| `LLM_<CHANNEL>_BASE_URL` | Variable or Secret | Use Secret for private gateways. |
| `LLM_<CHANNEL>_MODELS` | Variable or Secret | Comma-separated model list. |
| `LLM_<CHANNEL>_ENABLED` | Variable or Secret | Optional; defaults to enabled. |
| `LLM_<CHANNEL>_API_KEY` / `LLM_<CHANNEL>_API_KEYS` | Secret | API keys must be Secrets. |
| `LLM_<CHANNEL>_EXTRA_HEADERS` | Secret or Variable | Use Secret whenever it contains auth, tenant, organization, or private gateway data. |
| `LITELLM_CONFIG` | Variable or Secret | YAML file path. |
| `LITELLM_CONFIG_YAML` | Secret preferred | YAML content may contain private routing details. |
| `LLM_USAGE_HMAC_SECRET` | Secret | Optional high-entropy secret for cross-deployment usage-message HMAC comparison. |
| `LLM_USAGE_HMAC_KEY_VERSION` | Variable or Secret | Update when rotating `LLM_USAGE_HMAC_SECRET`. |

## OpenAI-Compatible And LiteLLM Rules

- OpenAI-compatible runtime model names normally use `openai/<model>`.
- Repository or organization prefixes such as `Qwen/...` or `deepseek-ai/...`
  are not automatically LiteLLM provider prefixes.
- If a model name already has a real LiteLLM provider prefix, keep it.
- YAML mode follows LiteLLM `model_list` / `litellm_params` semantics directly.

## Capability Checks

Runtime capability checks for JSON, tools, streaming, and vision can make real
LLM requests. Results are best-effort for the current account, key, model, and
endpoint. They do not write back to `.env` and do not block saving settings.

Potential costs and failures include token usage, image input fees, RPM/TPM
limits, insufficient balance, account permissions, unavailable models, regional
endpoints, provider compatibility layers, and LiteLLM conversion behavior.

## Diagnostics

| Code | Meaning | Fix |
| --- | --- | --- |
| `endpoint_not_found` | `/models` or chat endpoint path is missing. | Check the Base URL and avoid extra or missing provider-specific path segments. |
| `invalid_url` | Base URL contains unsafe or unsupported syntax. | Clear or correct `LLM_<CHANNEL>_BASE_URL`; use provider examples. |
| `model_access_denied` | Best-effort classification for disabled, unavailable, or unauthorized models. | Check the tested model in the provider console; adjust model order or fetch account-visible models. |
| `provider_prefix_mismatch` | LiteLLM provider prefix and channel protocol do not match. | Use `openai/<model>` for OpenAI-compatible channels. |
| `null_response` | LiteLLM returned no parseable response object. | Verify Chat Completions compatibility, model name, and endpoint. |
| `provider_blocked` | Provider or gateway policy appears to block the request. | Check provider policy, account region, gateway rules, or model entitlement. |

These diagnostic codes are best-effort runtime classifications, not official
cross-provider error-code mappings.

## Rollback

- Restore previous `.env` values for `LLM_*`, `LITELLM_MODEL`,
  `AGENT_LITELLM_MODEL`, `VISION_MODEL`, and `LITELLM_FALLBACK_MODELS`.
- To move from Channels back to legacy, delete or clear `LLM_CHANNELS` and keep
  legacy provider keys plus `LITELLM_MODEL`.
- To move from YAML back to Channels or legacy, remove `LITELLM_CONFIG` and
  `LITELLM_CONFIG_YAML`, then restart.
- Web/Desktop users can export a backup before changes and re-import it through
  `POST /api/v1/system/config/import`.

## Verification

```bash
python -m pytest tests/test_config_registry.py tests/test_config_validate_structured.py tests/test_local_cli_backend.py
```
