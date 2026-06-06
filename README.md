# Litmus

**The litmus test your resume takes before anyone reads it.**

![CI](https://github.com/Gauthambinoy20/litmus/actions/workflows/ci.yml/badge.svg)
![Security](https://github.com/Gauthambinoy20/litmus/actions/workflows/security.yml/badge.svg)
![CodeQL](https://github.com/Gauthambinoy20/litmus/actions/workflows/codeql.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![React](https://img.shields.io/badge/React-18-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Litmus is a **dual-axis resume scanner**: it scores a resume against a job description for **ATS keyword compatibility** (5 dimensions) and simultaneously for **AI-generated text risk** (19 detection signals), then turns every finding into an actionable fix. Results in under 3 seconds, fully functional offline and free — no API keys required.

> ✍️ TODO: my words — why I built this

---

## Screenshots

| Landing | Results |
|---|---|
| ![Landing](docs/screenshots/landing.png) | ![Results](docs/screenshots/results.png) |

| AI Detection Heatmap | Scan History |
|---|---|
| ![Heatmap](docs/screenshots/heatmap.png) | ![History](docs/screenshots/history.png) |

---

## Features

- **ATS engine** — keyword match, keyword placement, section completeness, formatting, semantic relevance
- **AI-detection engine** — 19 signals (sentence-length variance, opener diversity, banned-phrase density, adjective stacking, ML classifier, …) with a per-bullet risk heatmap
- **Fix generator** — every flagged issue becomes a prioritized, concrete suggestion with an example
- **Humanizer** — rewrites AI-flagged text via layered transforms (optional free ML paraphrase + rule-based)
- **Grammar & readability** — grammar checks, Flesch-Kincaid metrics
- **PDF/DOCX upload** and **bulk scanning**, **resume comparison**, **PDF report export**
- **Privacy by design** — stateless backend, nothing stored server-side; history lives in your browser

## Architecture

Diagrams (Mermaid, derived from the code) live in [`docs/`](docs/):
[Architecture](docs/architecture.md) · [Data flow](docs/data-flow.md) · [Scan sequence](docs/scan-sequence.md)

```
React 18 + TS (Vite, Tailwind)  →  FastAPI  →  engines/ (ATS · AI-detection · grammar ·
readability · humanizer · fix generator)  +  services/ (scan · export · analytics)
```

## Getting started

### Prerequisites
- Python 3.12+ · Node 22+ (or just Docker)

### Run with Docker

```bash
docker compose up --build
# frontend → http://localhost:3000 · backend → http://localhost:8000/docs
```

### Run locally

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m spacy download en_core_web_sm
python -c "import nltk; [nltk.download(p) for p in ['punkt','punkt_tab','stopwords','averaged_perceptron_tagger']]"
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm ci
npm run dev   # → http://localhost:5173
```

Optional: set `HUGGINGFACE_API_KEY` in `backend/.env` (see `.env.example`) to enable the free ML classifier/paraphrase layers. Everything works without it.

### Tests

```bash
cd backend && pytest tests/ --cov=app     # 116 tests
cd frontend && npx vitest run             # 29 tests
```

### Quality gates (same as CI)

```bash
cd backend && ruff check app/ tests/ && ruff format --check app/ tests/ && mypy app/ && bandit -r app/ -q -ll
cd frontend && npx eslint src --max-warnings 0 && npx prettier --check src && npx tsc --noEmit
```

## API

Interactive docs at `/docs` when the backend is running.

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/scan` | Full dual-axis scan (text input) |
| `POST /api/v1/scan/file` | Scan an uploaded PDF/DOCX |
| `POST /api/v1/scan/bulk` | Scan multiple files |
| `POST /api/v1/scan/quick` | Lightweight keyword-only scan |
| `POST /api/v1/compare` | Compare two resume versions |
| `POST /api/v1/humanize` | Rewrite AI-flagged text |
| `POST /api/v1/export/pdf` | Generate the PDF report |
| `POST /api/v1/keywords/extract` | Extract keyword sets from a JD |
| `GET /api/v1/health` · `GET /api/v1/stats` | Health & aggregate stats |

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

[MIT](LICENSE)
