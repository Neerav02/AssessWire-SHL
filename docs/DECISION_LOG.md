# Decision Log

## 2026-06-30

- Chose FastAPI because the assignment requires simple HTTP endpoints and deployment-friendly cold starts.
- Chose Pydantic-first development so malformed requests or responses fail loudly.
- Chose an explicit state machine because scope control, comparison grounding, and turn discipline should be deterministic.
- Chose hybrid retrieval because SHL catalog entries can be sparse and pure semantic search may over-rank vague personality or ability tests.
- Kept raw scrape output separate from cleaned catalog data for traceability.

