# AssessWise SHL Conversational Recommender

AssessWise is a FastAPI project scaffold for a conversational SHL assessment recommender. The design follows an explicit state machine, hybrid retrieval, strict response validation, and an evaluation harness so the system can be defended in a technical review instead of behaving like a loose RAG wrapper.

## What This Repo Contains

- FastAPI `/health` and `/chat` entry points.
- Pydantic request and response schemas.
- Conversation states for clarifying, retrieving, refining, comparing, and out-of-scope requests.
- Deterministic router scaffolding with room for a Groq/Gemini provider layer.
- Hybrid retrieval interfaces for structured filters plus semantic ranking.
- Catalog pipeline placeholders for raw scrape, cleaned catalog, and taxonomy enrichment.
- Evaluation harness for replay traces, schema validation, recall checks, and adversarial probes.
- Approach and decision-log documentation templates.

## Project Structure

```text
.
├── data/
│   ├── catalog/
│   ├── embeddings/
│   └── traces/
├── docs/
├── prompts/
├── scripts/
├── src/
│   └── assesswise_shl/
└── tests/
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn assesswise_shl.api.main:app --reload
```

Then verify:

```powershell
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Environment Variables

Copy `.env.example` to `.env` and add real API keys only on your local machine or deployment platform.

```text
GROQ_API_KEY=
GEMINI_API_KEY=
```

## Current Status

This is the proper starter structure for the project. The next implementation step is to provide the exact assignment response schema and the 10 official traces, then scrape and normalize the SHL Individual Test Solutions catalog into `data/catalog/catalog_clean.json`.

