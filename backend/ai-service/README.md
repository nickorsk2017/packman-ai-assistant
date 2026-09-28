# PackMan AI Service

Device descriptions, tags, and vector search (Qdrant).

## Setup

```bash
uv sync
```

## Run the service

```bash
uv run packman-ai-service
```

## Qdrant client & dashboard

- **Python client**: `qdrant-client` is already in dependencies (see `pyproject.toml`). Install with `uv sync`.
- **Why the dashboard shows no collections**: The app can use either **embedded** storage (`data/qdrant`) or a **Qdrant server** (Docker). Embedded storage uses a different format; the server dashboard cannot read it, so the collection list stays empty until you use the server.

- **To see the collection list in the dashboard** (e.g. http://localhost:6333/dashboard#/collections):

  1. **Start the Qdrant server** (before the AI service):
     ```bash
     uv run packman-run-qdrant
     ```
     Or: `docker compose up -d`

  2. **Point the app at the server** — in `.env` add:
     ```env
     QDRANT_URL=http://localhost:6333
     ```

  3. **Restart the AI service** and **index a device** from the app (e.g. Add Device on the search page). The `devices` collection will be created on the server and will appear in the dashboard.

  Then open:

  - **Dashboard**: http://localhost:6333/dashboard  
  - **REST API**: http://localhost:6333  

  Without `QDRANT_URL`, the app uses embedded storage at `data/qdrant`; that data is not visible in the server dashboard.

  Stop the server:

  ```bash
  docker compose down
  ```

## Quality evals (DeepEval)

The `evals/` suite measures the quality of the Add Device and Search pipelines with
[DeepEval](https://github.com/confident-ai/deepeval). Every metric has a pass/fail threshold;
a metric below its threshold fails the run.

### Run

```bash
make eval
make eval-add
make eval-search
```

`make eval` runs everything, `make eval-add` and `make eval-search` run one pipeline.
Dependencies are in the optional extra `eval` (`uv sync --extra eval`).

### Environment

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Pipeline calls and the LLM judge |
| `EVAL_JUDGE_MODEL` | Judge model (default: the service model) |
| `EVAL_QDRANT_COLLECTION` | Eval collection, default `devices_eval`; `devices` is refused |
| `EVAL_QDRANT_PATH` | Embedded storage for evals when `QDRANT_URL` is unset, default `data/qdrant_eval` |
| `EVAL_THRESHOLD_<KEY>` | Override a threshold from `evals/config.py`, e.g. `EVAL_THRESHOLD_FAITHFULNESS=0.9` |

Search evals drop and re-seed the eval collection from `evals/datasets/devices_catalog.json`
through the real indexing pipeline. The working `devices` collection is never read or written.

### Reports

- `evals/reports/summary-<timestamp>.json`: per pipeline, stage and metric: mean and min score,
  pass rate, failed cases; stage latency; judge cost; every individual result with its reason.
- `evals/reports/` also receives DeepEval native run files (`DEEPEVAL_RESULTS_FOLDER`).
- The terminal prints the same summary table at the end of the run.

### Datasets

| File | Content |
|------|---------|
| `evals/datasets/devices_catalog.json` | Golden catalog: seller descriptions, prices, expected traits and specifications |
| `evals/datasets/add_device_cases.json` | Web research cases with reference facts (one non-existent device), devices for description evals |
| `evals/datasets/search_cases.json` | Search prompts with expected traits and relevant devices, including negative cases |

### Metrics

| Pipeline / stage | Metric | Type | Meaning |
|------------------|--------|------|---------|
| Add Device / research | Found Detection | deterministic | `found` matches the golden flag; a found device cites sources |
| Add Device / research | Hallucination | LLM judge | Share of facts contradicting the reference (lower is better) |
| Add Device / research | Research Correctness (GEval) | LLM judge | Specs agree with the reference, no specs from other models |
| Add Device / research | Research Completeness (GEval) | LLM judge | Share of golden key facts covered |
| Add Device / specs | Field Accuracy (traits) | deterministic | Exact match of traits used as search filters |
| Add Device / specs | Field Accuracy (specifications) | deterministic | Normalized substring match of free-text specs |
| Add Device / short description | Faithfulness | LLM judge | Claims supported by seller description, specs and price |
| Add Device / short description | Description Quality (GEval) | LLM judge | Format and content rules of the description prompt |
| Search / traits | Field Accuracy (traits) | deterministic | Traits extracted from the prompt; explicit `null` means the filter must not be set |
| Search / retrieval, rerank | Precision@k, Recall@k, MRR | deterministic | Returned names vs golden relevant devices |
| Search / retrieval, rerank | Contextual Precision, Recall, Relevancy | LLM judge | Ranking and relevance of returned device texts |

`retrieval` is the vector search output (top k, before rerank), `rerank` is the final API response.
Negative cases (no relevant device) are scored only after rerank: the result must be empty.

Cost: one full run makes roughly 150-250 LLM calls including 3 web-search calls.
