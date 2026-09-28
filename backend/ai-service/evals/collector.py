"""Collects metric scores and stage latencies across the session for the summary report."""

import importlib
import time
from contextlib import contextmanager
from statistics import mean

from deepeval import assert_test
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

RESULTS: list[dict] = []
LATENCIES: list[dict] = []

# assert_test() evaluates copies of the metrics and does not return its TestResult.
# Wrap the executors it calls to capture metrics_data of the last evaluated test case.
_LAST_RESULTS: list = []
_deepeval_evaluate = importlib.import_module("deepeval.evaluate.evaluate")

if not hasattr(_deepeval_evaluate, "a_execute_test_cases") or not hasattr(
    _deepeval_evaluate, "execute_test_cases"
):
    raise ImportError("Unsupported deepeval version: assert_test executors not found")

_orig_a_execute = _deepeval_evaluate.a_execute_test_cases
_orig_execute = _deepeval_evaluate.execute_test_cases


async def _a_execute_capture(*args, **kwargs):
    results = await _orig_a_execute(*args, **kwargs)
    _LAST_RESULTS[:] = results
    return results


def _execute_capture(*args, **kwargs):
    results = _orig_execute(*args, **kwargs)
    _LAST_RESULTS[:] = results
    return results


_deepeval_evaluate.a_execute_test_cases = _a_execute_capture
_deepeval_evaluate.execute_test_cases = _execute_capture


@contextmanager
def timed(pipeline: str, stage: str, case_id: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        LATENCIES.append({
            "pipeline": pipeline,
            "stage": stage,
            "case": case_id,
            "seconds": round(time.perf_counter() - start, 3),
        })


def _record(pipeline: str, stage: str, case_id: str, metrics: list[BaseMetric]) -> None:
    metrics_data = (_LAST_RESULTS[0].metrics_data or []) if _LAST_RESULTS else []
    by_name = {d.name: d for d in metrics_data}
    for index, metric in enumerate(metrics):
        data = by_name.get(metric.__name__) or (metrics_data[index] if index < len(metrics_data) else None)
        RESULTS.append({
            "pipeline": pipeline,
            "stage": stage,
            "case": case_id,
            "metric": data.name if data else metric.__name__,
            "score": data.score if data else None,
            "threshold": metric.threshold,
            "success": bool(data.success) if data else False,
            "reason": data.reason if data else None,
            "error": data.error if data else "metric was not evaluated",
            "cost": data.evaluation_cost if data else None,
        })


def evaluate(
    test_case: LLMTestCase,
    metrics: list[BaseMetric],
    *,
    pipeline: str,
    stage: str,
    case_id: str,
) -> None:
    """Run DeepEval assert_test and record every metric result, pass or fail."""
    test_case.name = test_case.name or f"{pipeline}/{stage}/{case_id}"
    _LAST_RESULTS.clear()
    try:
        assert_test(test_case, metrics)
    finally:
        _record(pipeline, stage, case_id, metrics)


def summary() -> dict:
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for row in RESULTS:
        groups.setdefault((row["pipeline"], row["stage"], row["metric"]), []).append(row)
    metrics = []
    for (pipeline, stage, metric), rows in sorted(groups.items()):
        scores = [r["score"] for r in rows if r["score"] is not None]
        metrics.append({
            "pipeline": pipeline,
            "stage": stage,
            "metric": metric,
            "n": len(rows),
            "mean_score": round(mean(scores), 4) if scores else None,
            "min_score": round(min(scores), 4) if scores else None,
            "pass_rate": round(sum(r["success"] for r in rows) / len(rows), 4),
            "threshold": rows[0]["threshold"],
            "failed_cases": [r["case"] for r in rows if not r["success"]],
        })
    lat_groups: dict[tuple[str, str], list[float]] = {}
    for row in LATENCIES:
        lat_groups.setdefault((row["pipeline"], row["stage"]), []).append(row["seconds"])
    latency = [
        {
            "pipeline": p,
            "stage": s,
            "n": len(v),
            "mean_seconds": round(mean(v), 3),
            "max_seconds": round(max(v), 3),
        }
        for (p, s), v in sorted(lat_groups.items())
    ]
    cost = sum(r["cost"] or 0 for r in RESULTS)
    return {"metrics": metrics, "latency": latency, "judge_cost_usd": round(cost, 4)}
