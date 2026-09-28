"""Paths and pass/fail thresholds for the DeepEval suite."""

import os
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
DATASETS_DIR = EVALS_DIR / "datasets"
REPORTS_DIR = EVALS_DIR / "reports"

PRODUCTION_COLLECTION = "devices"

# Score thresholds in [0, 1]. For "hallucination" the score must be <= threshold,
# for every other metric the score must be >= threshold.
# Override any value with env EVAL_THRESHOLD_<KEY>, e.g. EVAL_THRESHOLD_FAITHFULNESS=0.9
_DEFAULT_THRESHOLDS: dict[str, float] = {
    # Add Device: web research
    "research_found": 1.0,
    "hallucination": 0.3,
    "research_correctness": 0.6,
    "research_completeness": 0.6,
    # Add Device: specs + short description
    "specs_traits_accuracy": 0.8,
    "specs_specifications_accuracy": 0.7,
    "faithfulness": 0.8,
    "description_quality": 0.6,
    # Search: trait extraction
    "search_traits_accuracy": 0.8,
    # Search: retrieval (vector search, top k)
    "retrieval_precision_at_k": 0.2,
    "retrieval_recall_at_k": 0.8,
    "retrieval_mrr": 0.7,
    "retrieval_contextual_precision": 0.6,
    "retrieval_contextual_recall": 0.6,
    "retrieval_contextual_relevancy": 0.3,
    # Search: after LLM rerank (final response)
    "rerank_precision_at_k": 0.5,
    "rerank_recall_at_k": 0.8,
    "rerank_mrr": 0.7,
    "rerank_contextual_precision": 0.6,
    "rerank_contextual_recall": 0.6,
    "rerank_contextual_relevancy": 0.5,
}


def threshold(key: str) -> float:
    raw = os.getenv(f"EVAL_THRESHOLD_{key.upper()}")
    if raw is not None:
        return float(raw)
    return _DEFAULT_THRESHOLDS[key]
