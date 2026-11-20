# Meeting Bot

[![CI](https://github.com/waleedarif1011/Meeting-Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/waleedarif1011/Meeting-Bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Meeting Bot** turns a raw meeting transcript into answers you can use — summaries, action items, decisions, topics, and who was in the room — through a simple chat UI.

> **Live Demo:** Not published yet. Prefer **one deploy**: host `python server.py` on Railway or Render (Flask serves the UI + API). After it is live, put that HTTPS URL here. Optional split path: Vercel static `frontend/` + separate API via `?api=`.

No LLM API key required — extraction and summarization run with Sumy TextRank + light NLP rules.

![Meeting Bot demo](assets/meeting-bot-demo.png)

## What you can do

1. Paste a transcript **or** click **Load sample meeting**
2. Ask natural questions, for example:
   - “Summarize the meeting”
   - “What were the action items?”
   - “What decisions were made?”
   - “Who attended?”
   - “What topics came up?”

## Features

- One-click **Load sample meeting** for instant demos
- TextRank summarization (Sumy + NLTK) — zero external AI keys
- Extraction of attendees, action items, decisions, and topics
- Session chat over a small Flask API
- **Single process** can serve UI + API (Railway/Render)
- Optional split: static UI on Vercel + API elsewhere

## Architecture

```
Single deploy (recommended)
┌─────────────────────────────────────────┐
│  Flask (Railway / Render)               │
│  /          → frontend/index.html       │
│  /health /sample /upload /chat → API    │
│  chatbot/engine.py (Sumy TextRank)      │
└─────────────────────────────────────────┘

Optional split
┌─────────────────────┐       HTTPS        ┌──────────────────────┐
│  Frontend (Vercel)  │ ─────────────────► │  Flask API only      │
│  ?api=https://…     │                    │  Railway / Render    │
└─────────────────────┘                    └──────────────────────┘
```

API base resolution (see [`frontend/config.js`](frontend/config.js)): query → meta → inject → localStorage → same-origin (or `http://localhost:5000` when the UI is on port 3000).

## Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Open **http://localhost:5000** — Flask serves the UI and API together.

Optional split for frontend-only iteration:

```bash
cd frontend && python -m http.server 3000
```

Then open http://localhost:3000 (config defaults API to `http://localhost:5000`). Or use `./start-dev.sh` inside the Dev Container ([DEV_SETUP.md](DEV_SETUP.md)).

## API

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check (`{"status":"ok"}`) |
| `GET` | `/sample` | Built-in Q4 planning transcript |
| `POST` | `/upload` | `{ "transcript": "...", "session_id": "..." }` |
| `POST` | `/chat` | `{ "message": "...", "session_id": "..." }` → `{ "response": "..." }` |

CORS is enabled. Bind port via `PORT` (default `5000`).

## Deploy

### Recommended: single host (Railway or Render)

Flask serves `frontend/` and the JSON API from one process — one public URL is the Live Demo.

**Railway**

1. [Railway](https://railway.app) → New project → Deploy from GitHub → this repo.
2. Start command: `python server.py` (or use the included `Procfile`).
3. Python **3.11** if prompted (`runtime.txt` pins `3.11.9`).
4. Open the public HTTPS URL → **Load sample meeting**.

**Render**

1. [Render](https://render.com) → New **Web Service** → connect this repo.
2. Build: `pip install -r requirements.txt`
3. Start: `python server.py`
4. Free/starter instance is enough for demos.

Confirm:

```bash
curl https://YOUR-HOST/health
# → {"status":"ok"}
```

Then set the Live Demo line at the top of this README to `https://YOUR-HOST`.

### Optional: Vercel UI + separate API

1. Deploy the Flask API on Railway/Render as above.
2. Import this repo in [Vercel](https://vercel.com) (Framework Preset **Other**; `vercel.json` serves `frontend/`).
3. Open `https://YOUR-VERCEL-URL/?api=https://YOUR-API-HOST`  
   (or set `<meta name="api-base-url" content="https://YOUR-API-HOST">` in `frontend/index.html`).

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

CI runs the same suite on every push/PR via [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Project layout

```
meeting-bot/
├── frontend/           # Static UI (also served by Flask at /)
│   ├── config.js       # API base resolution
│   ├── index.html
│   ├── script.js
│   └── style.css
├── chatbot/
│   ├── engine.py       # NLP extraction + TextRank
│   └── README.md
├── assets/             # README demo screenshot
├── tests/
├── server.py           # Flask API + static UI
├── vercel.json         # Optional Vercel static frontend
├── Procfile            # Railway/Render
└── requirements.txt
```

More detail: [chatbot/README.md](chatbot/README.md) · [DEV_SETUP.md](DEV_SETUP.md)

## Suggested GitHub topics

`meeting-notes` · `nlp` · `flask` · `textrank` · `portfolio`

## License

MIT — see [LICENSE](LICENSE).
