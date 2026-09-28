# TASK — 2026-09-27-deepeval-metrics
owner: Engineer
immutable: true

## Requirements
- R1: Add a DeepEval-based evaluation suite to `backend/ai-service` that measures quality of the Add Device pipeline and the Search pipeline.
- R2: Add Device / web research (`research_device`): measure factual grounding of facts against sources, completeness vs. a golden reference, and correct found / not-found detection (including a non-existent device).
- R3: Add Device / specs + description: measure field-level accuracy of extracted traits and specifications (`get_device_specs_by_name`) against golden values, and faithfulness / no-hallucination of `get_short_description` against seller description + extracted specs.
- R4: Search / trait extraction (`get_specifications_by_user_prompt`): measure field-level accuracy against golden traits per user prompt.
- R5: Search / retrieval + rerank (vector search + `rerank_devices`): measure DeepEval contextual metrics (precision, recall, relevancy) and deterministic ranking metrics (Precision@k, Recall@k, MRR) against golden relevant device names; report retrieval-only and post-rerank results separately.
- R6: Search evaluation runs against a dedicated Qdrant collection (`devices_eval`) seeded from a golden device catalog by the suite itself; the working `devices` collection is never read or written.
- R7: Run via pytest + `deepeval test run`, each metric with a pass/fail threshold; entry point `make eval` (plus per-pipeline targets); results persisted as JSON under `backend/ai-service/evals/reports/`.
- R8: Golden datasets are versioned JSON files in the repo (device catalog, add-device cases, search cases).

## Acceptance
- A1: `make eval` runs the whole suite; `make eval-add` and `make eval-search` run each pipeline separately.
- A2: Each of R2..R5 has at least one DeepEval metric with an explicit threshold, and a failing threshold fails the pytest run.
- A3: Running search evals leaves the `devices` collection untouched.
- A4: The AI service still imports and starts after the dependency changes (`uv run python -c "import app.main"`).
- A5: README in `backend/ai-service` documents how to run evals, required env, and what each metric means.

## Constraints
- English only in files.
- Judge model is OpenAI via existing `OPENAI_API_KEY`; judge model name configurable via settings/env.
- No Confident AI upload; local results only.
- No changes to production behavior of the device endpoints.
