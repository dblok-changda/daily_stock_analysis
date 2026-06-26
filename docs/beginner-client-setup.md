# Beginner Client Setup

This guide is for users who want a working local client without reading the full
deployment guide first.

## 1. Install Dependencies

Use Python 3.10 or newer.

```bash
pip install -r requirements.txt
```

For the web client:

```bash
cd apps/dsa-web
npm ci
```

## 2. Configure Environment Variables

Copy the example file and fill in only the providers you plan to use.

```bash
cp .env.example .env
```

Minimum useful settings:

- `STOCK_LIST`: comma-separated symbols such as `600519,hk00700,AAPL`.
- One LLM provider key, for example `OPENAI_API_KEY`, `GEMINI_API_KEY`, or a
  configured OpenAI-compatible endpoint.
- Optional search keys such as `ANSPIRE_API_KEYS`, `SERPAPI_API_KEY`,
  `TAVILY_API_KEY`, `BOCHA_API_KEY`, `BRAVE_SEARCH_API_KEY`, or SearXNG base
  URLs.
- Optional notification channel settings if you want reports delivered outside
  the web UI.

## 3. Run A Local Analysis

```bash
python main.py --dry-run
python main.py --stocks 600519,hk00700,AAPL
```

Use `--dry-run` first to validate configuration without sending notifications.

## 4. Start The API And Web Client

Backend:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Web:

```bash
cd apps/dsa-web
npm run dev
```

Open the Vite URL shown in the terminal. The web client expects the backend to be
available through its configured API base URL.

## 5. Troubleshooting

- If LLM calls fail, verify the selected provider key and model configuration.
- If news is missing, configure at least one search provider.
- If stock names do not resolve, refresh the stock index and rerun loader tests.
- If notifications fail, run the notification diagnostics before changing
  runtime code.

For complete configuration details, see `docs/full-guide.md`.
