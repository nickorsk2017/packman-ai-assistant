# EXEC — 2026-09-27-deepeval-metrics

## v1

### Summary by step
- P1: `pyproject.toml` extra `eval` (`pytest`, `deepeval>=4.2,<5`), pins `pydantic==2.11.7`, `pydantic-settings==2.10.1`; `uv.lock` regenerated (deepeval 4.2.6). `app/config.py`: `eval_judge_model`, `eval_qdrant_collection`, `eval_qdrant_path`.
- P2: `evals/datasets/devices_catalog.json` (12 devices: 5 phones incl. foldable, 3 laptops incl. 2 dual-screen, 1 MacBook, 2 tablets, 1 camera), `add_device_cases.json` (3 research + 1 non-existent, 5 description devices), `search_cases.json` (12 cases, 2 negative). Vocabulary taken from `TRAITS_FIELDS_DEVICE`.
- P3: `evals/config.py` (paths, threshold table, env override), `evals/judge.py` (deepeval `OpenAIModel`; `GPTModel` is deprecated in 4.x), `evals/datasets.py`, `evals/metrics.py` (FieldAccuracy, Ranking, FoundDetection).
- P4: `evals/conftest.py` (settings override + guard, `catalog_outputs` cache, `seeded_index`, summary JSON + terminal table). Result capture lives in `evals/collector.py` (helper module importable by tests).
- P5: `evals/test_add_device.py`: research (4), specs (12), short description (5).
- P6: `evals/test_search.py`: trait extraction (12), ranking x {retrieval, rerank} (24, 2 retrieval negatives skipped).
- P7: Makefile targets `eval`, `eval-add`, `eval-search` + help; `.gitignore` for reports and `.deepeval/`; `evals/reports/.gitkeep`.
- P8: README section "Quality evals (DeepEval)".

### Implementation notes (no design change)
- N1 deepeval `assert_test` evaluates copies of metrics (`copy_metrics` rebuilds from constructor args) and does not return results. Collector wraps `a_execute_test_cases` / `execute_test_cases` in `deepeval.evaluate.evaluate` to capture `metrics_data`; fails at import if those symbols disappear (version pinned <5). Custom metrics store every constructor arg as an attribute.
- N2 Short description judged on raw HTML output (quality criteria include tag rules).

### Checks (P9)
- `uv sync --extra eval` (isolated venv outside repo; repo `.venv` belongs to macOS host, untouched): OK.
- `import app.main` with pydantic 2.11.7: OK (A4).
- `py_compile evals/*.py`: OK. `pytest evals --collect-only`: 57 tests collected.
- Offline metric check through `assert_test`: FieldAccuracy exact/contains, Ranking P@k/R@k/MRR, negative case, FoundDetection, summary aggregation: scores as expected; failing metric raises AssertionError and is still recorded.
- Guard: `EVAL_QDRANT_COLLECTION=devices` -> `UsageError` at conftest load (A3).
- `deepeval test run evals/test_add_device.py -k Zorbix` without key: runner wiring works, test fails with `OPENAI_API_KEY is not set` as expected.
- Live `make eval`: NOT RUN. Sandbox has no egress to api.openai.com. Must be run on the Engineer machine.

### Changed files
- Makefile
- backend/ai-service/.gitignore
- backend/ai-service/README.md
- backend/ai-service/app/config.py
- backend/ai-service/pyproject.toml
- backend/ai-service/uv.lock
- backend/ai-service/evals/{__init__,config,judge,datasets,metrics,collector,conftest,test_add_device,test_search}.py
- backend/ai-service/evals/datasets/{devices_catalog,add_device_cases,search_cases}.json
- backend/ai-service/evals/reports/.gitkeep
