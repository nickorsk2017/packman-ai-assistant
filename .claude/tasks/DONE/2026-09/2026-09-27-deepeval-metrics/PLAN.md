# PLAN — 2026-09-27-deepeval-metrics

## v1

### Decisions
- D1 Location: new package `backend/ai-service/evals/` (pytest root for `deepeval test run`); not shipped in the `app` wheel.
- D2 Dependency: `deepeval>=4.2,<5` in a new optional extra `eval` (with `pytest`). deepeval 4.x requires `pydantic>=2.11.7` and `pydantic-settings>=2.10.1`; bump pins to `pydantic==2.11.7`, `pydantic-settings==2.10.1` (fastapi 0.115.6 supports pydantic <3). Regenerate `uv.lock`. Risk covered by A4 check.
- D3 Judge: deepeval `GPTModel` built from `settings.openai_api_key` and new setting `eval_judge_model` (default = model used by the service). One shared factory in `evals/judge.py`.
- D4 Isolation (R6/A3): evals override `settings.qdrant_collection` to new setting `eval_qdrant_collection` (default `devices_eval`) BEFORE `vector_store_service` builds its store; in embedded mode also override `qdrant_path` to `data/qdrant_eval` (embedded storage is lock-exclusive with a running service). A hard guard aborts the session if the effective collection equals `devices`. Collection is dropped and re-seeded once per session.
- D5 Seeding: catalog devices are indexed through the real pipeline (`get_device_specs_by_name` -> `get_short_description` -> `vector_store_service.add_device`) with seller descriptions from the golden catalog, so search is evaluated against what production would index. No web research during seeding (deterministic, cheaper).
- D6 Search flow: evals reproduce the 3 steps of `GET /device/search` (trait extraction -> `vector_store_service.search` -> `rerank_devices`) importing `SEARCH_CANDIDATES_MULTIPLIER` / `SEARCH_CANDIDATES_MAX` from `app.api.device`; production code unchanged. Two stages are captured per case: `retrieval` (pre-rerank, truncated to k) and `rerank` (final).
- D7 Custom deterministic metrics (subclass `deepeval.metrics.BaseMetric`, sync + async measure, score in [0,1], threshold):
  - `FieldAccuracyMetric`: compares actual vs golden dict; only fields present in golden are scored (explicit `null` in golden = must be absent/unknown); case/whitespace-insensitive string compare, numeric tolerance for numbers, substring-tolerant mode for free-text spec fields; `score_breakdown` lists per-field hits.
  - `RankingMetric(kind=precision_at_k|recall_at_k|mrr)`: golden relevant names vs returned names (normalized); empty golden + empty result = 1.0 (negative cases).
  - `FoundDetectionMetric`: research `found` flag vs golden `expect_found`; also fails when `found` is true with no sources.
- D8 LLM-judge metrics per pipeline:
  - Research (R2): `HallucinationMetric` (context = golden reference facts; pass if score <= threshold), `GEval` "Research Correctness" (actual vs expected_output: no wrong specs), `GEval` "Research Completeness" (covers key golden facts), `FoundDetectionMetric`.
  - Specs (R3): `FieldAccuracyMetric` on traits, `FieldAccuracyMetric` on specifications.
  - Short description (R3): `FaithfulnessMetric` (retrieval_context = seller description, extracted specs JSON, price), `GEval` "Description Quality" with criteria derived from `GET_SHORT_DEVICE_DESCRIPTION_PROMPT` rules.
  - Trait extraction (R4): `FieldAccuracyMetric` on `DeviceTraits`; golden sets `brand/os/category` explicitly (null when unspecified) because they are hard Qdrant filters and spurious values zero out recall.
  - Retrieval + rerank (R5): per stage `ContextualPrecisionMetric`, `ContextualRecallMetric`, `ContextualRelevancyMetric` (retrieval_context = ranked device page texts via `build_page_content`, expected_output = golden relevant device summary) + `RankingMetric` x3.
- D9 Thresholds: single table in `evals/config.py`, overridable by env `EVAL_THRESHOLD_<METRIC>`; initial baselines: field accuracy 0.8, faithfulness 0.8, hallucination <=0.3, GEval 0.6, contextual 0.6, precision@k 0.5, recall@k 0.8, MRR 0.7, found detection 1.0.
- D10 Reporting (R7): `DEEPEVAL_RESULTS_FOLDER=evals/reports` (deepeval native JSON per run) + a `pytest_sessionfinish` hook writing `evals/reports/summary-<timestamp>.json`: per pipeline/stage/metric mean score, pass rate, n, plus per-stage wall-clock latency. Reports dir git-ignored except `.gitkeep`.
- D11 Datasets (R8), `evals/datasets/`:
  - `devices_catalog.json`: ~12 devices across phones (incl. foldable), laptops (incl. dual-screen), tablets, wearables, audio, consoles; each: name, price, seller description, golden traits, golden specifications (subset).
  - `add_device_cases.json`: research cases (>=3 real devices with reference facts, 1 non-existent device with expect_found=false); specs/description cases reference catalog entries.
  - `search_cases.json`: ~10 prompts covering brand, os, category, form factor, dual screen, price cap, combined constraints, and >=1 negative (no match); each: prompt, k, optional max_price, golden traits, relevant device names.
- D12 Entry points (R7/A1): Makefile targets `eval`, `eval-add`, `eval-search` running `uv run --extra eval deepeval test run <path>` in `backend/ai-service` with the results folder env. pytest markers `add_device` / `search`.

### Steps
- P1 Deps + settings: pyproject (D2, extra `eval`), `uv.lock`, `app/config.py` new settings `eval_judge_model`, `eval_qdrant_collection` (D3/D4). No other `app/` changes.
- P2 Datasets (D11) after reading `app/prompts/device_prompts.py` so golden values use the vocabulary the prompts enforce (categories, form factors, os names).
- P3 `evals/config.py` (thresholds, paths), `evals/judge.py` (D3), `evals/metrics.py` (D7), `evals/datasets.py` loader (typed via pydantic).
- P4 `evals/conftest.py`: env/settings override + guard (D4), session fixture seeding `devices_eval` (D5), result collector + summary hook (D10), markers.
- P5 `evals/test_add_device.py` (R2, R3) parametrized per case with `assert_test`.
- P6 `evals/test_search.py` (R4, R5) parametrized per case and stage (D6).
- P7 Makefile targets + help lines (D12); `evals/reports/.gitkeep` + ignore rule.
- P8 README section: run commands, env (`OPENAI_API_KEY`, optional `QDRANT_URL`, `EVAL_JUDGE_MODEL`, threshold overrides), metric glossary, cost note.
- P9 Checks: `uv lock` + `uv sync --extra eval`, `uv run python -c "import app.main"` (A4), `uv run --extra eval pytest evals --collect-only` (collection without API calls), `py_compile` on all new files. Live `make eval` only if `OPENAI_API_KEY` is available; record outcome in EXEC.md.

### Risks
- K1 pydantic bump could change validation behavior in service schemas -> A4 import check + schemas use only basic BaseModel features.
- K2 LLM judge variance -> thresholds are baselines, env-overridable; deterministic metrics carry the hard signal.
- K3 D6 duplicates endpoint orchestration -> drift possible if the endpoint changes; constants imported, not copied.
- K4 Cost: research cases use web search; kept to 4 cases.
