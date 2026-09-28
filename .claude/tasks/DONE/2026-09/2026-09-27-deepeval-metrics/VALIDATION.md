# VALIDATION — 2026-09-27-deepeval-metrics

## v1
result: PASS
validation_version: 1
- R1 PASS: suite in backend/ai-service/evals, extra `eval`, deepeval 4.2.6 locked.
- R2 PASS: research test: FoundDetection (incl. non-existent device, sources required), Hallucination vs reference, GEval correctness and completeness.
- R3 PASS: FieldAccuracy traits (exact) and specifications (contains) on 12 catalog devices; Faithfulness + GEval quality on 5 descriptions.
- R4 PASS: FieldAccuracy on DeviceTraits for 12 prompts; explicit nulls enforce absent hard filters.
- R5 PASS: Precision@k, Recall@k, MRR + Contextual Precision/Recall/Relevancy per stage (retrieval, rerank); negatives judged after rerank only.
- R6/A3 PASS: collection overridden before vector store init, embedded path separated, `devices` rejected at conftest load (verified).
- R7/A1/A2 PASS: make eval, eval-add, eval-search call `deepeval test run`; thresholds in evals/config.py, env-overridable; failing metric raises AssertionError (verified offline); summary JSON + DeepEval results folder in evals/reports.
- R8 PASS: 3 versioned JSON datasets.
- A4 PASS: `import app.main` OK with pydantic 2.11.7.
- A5 PASS: README section with run, env, reports, datasets, metric glossary.
- Constraints PASS: English only (0 Cyrillic in changed files and artifacts); app/ change limited to 3 new settings; no Confident AI upload; endpoint behavior unchanged.
- Note (non-blocking): live LLM run not executed in sandbox (no egress to OpenAI); baseline scores come from the first `make eval` on the Engineer machine. Thresholds are initial baselines (PLAN D9, K2).
issues: []
