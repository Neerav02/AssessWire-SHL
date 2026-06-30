# Risk Checklist

- [ ] `/health` returns exactly `{"status": "ok"}`.
- [ ] Every `/chat` response validates against the required schema.
- [ ] Every recommendation URL comes from the cleaned catalog.
- [ ] The scraper includes only Individual Test Solutions.
- [ ] The agent asks one focused clarification question when signal is insufficient.
- [ ] Refinement preserves prior conversation constraints.
- [ ] Comparison mode uses only catalog records.
- [ ] Prompt-injection attempts return an out-of-scope refusal.
- [ ] Official traces are replayed before submission.
- [ ] Trace zip URL is obtained from the assignment provider because the PDF shows only placeholder text.
- [ ] Recall@10 and hallucination checks are reported in the approach document.
