# AssessWise SHL Conversational Recommender

AssessWise is a FastAPI project scaffold for a conversational SHL assessment recommender. The design follows an explicit state machine, hybrid retrieval, strict response validation, and an evaluation harness so the system can be defended in a technical review instead of behaving like a loose RAG wrapper.

## What This Repo Contains

- FastAPI `/health` and `/chat` entry points.
- Pydantic request and response schemas matching the assignment PDF.
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

## Assignment API Contract

`POST /chat`

```json
{
  "messages": [
    {"role": "user", "content": "Hiring a Java developer who works with stakeholders"},
    {"role": "assistant", "content": "Sure. What is seniority level?"},
    {"role": "user", "content": "Mid-level, around 4 years"}
  ]
}
```

Response:

```json
{
  "reply": "Got it. Here are 5 assessments that fit a mid-level Java dev with stakeholder needs.",
  "recommendations": [
    {"name": "Java 8 (New)", "url": "https://www.shl.com/...", "test_type": "K"}
  ],
  "end_of_conversation": false
}
```

The public response must not include internal routing fields.

## Environment Variables

Copy `.env.example` to `.env` and add real API keys only on your local machine or deployment platform.

```text
GROQ_API_KEY=
GEMINI_API_KEY=
```

Do not commit real API keys. If a key has been pasted into chat or shared anywhere public, regenerate it before deployment.

## Render Deployment

1. Push this repository to GitHub.
2. In Render, create a new Web Service from that repository.
3. Use the included `render.yaml` or set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn assesswise_shl.api.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render:
   - `GROQ_API_KEY`
   - `APP_ENV=production`
   - `PYTHONPATH=src`

## Current Status

The exact response schema has been aligned to the PDF. The PDF includes the SHL catalog URL but the public conversation traces and submission form are shown only as placeholder text (`Link`), so those files still need to be obtained from the assignment portal or provider.
