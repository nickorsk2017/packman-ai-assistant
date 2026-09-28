"""Deterministic DeepEval metrics: field accuracy, ranking quality, found detection.

Custom metrics read their inputs from `LLMTestCase.metadata`, so the same test case
can also carry natural-language fields for LLM-judge metrics.
DeepEval re-creates metrics from their constructor arguments (`copy_metrics`), so every
constructor argument is stored under an attribute of the same name.
"""

import re
from typing import Any, Literal

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

IGNORED_VALUES = (None, "", "unknown", "any", "null", "none", "n/a")
NUMERIC_TOLERANCE = 0.01


def _norm_text(value: Any) -> str:
    return re.sub(r"[^a-z0-9.]", "", str(value).lower())


def _is_empty(value: Any) -> bool:
    return value in IGNORED_VALUES or (isinstance(value, str) and value.strip().lower() in IGNORED_VALUES)


def _norm_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


class _DeterministicMetric(BaseMetric):
    """Base for metrics without an LLM judge: sync and async share one implementation."""

    metric_name = "Deterministic"

    def __init__(self, threshold: float, name: str | None = None) -> None:
        self.threshold = threshold
        self.include_reason = True
        self.async_mode = False
        self.strict_mode = False
        self.verbose_mode = False
        self.evaluation_model = None
        self.evaluation_cost = 0.0
        if name:
            self.metric_name = name

    def _compute(self, test_case: LLMTestCase) -> tuple[float, str, dict]:
        raise NotImplementedError

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        try:
            self.score, self.reason, self.score_breakdown = self._compute(test_case)
            self.success = self.is_successful()
        except Exception as error:
            self.error = str(error)
            self.score, self.success = 0.0, False
            raise
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        if self.error is not None or self.score is None:
            return False
        return self.score >= self.threshold

    @property
    def __name__(self) -> str:
        return self.metric_name


class FieldAccuracyMetric(_DeterministicMetric):
    """Share of golden fields the pipeline got right.

    metadata[group] = {"actual": {...}, "expected": {...}}. Only fields present in
    `expected` are scored; an explicit null in `expected` means the field must be empty.
    mode "exact": normalized equality (traits used as filters).
    mode "contains": normalized substring either way (free-text specifications).
    """

    def __init__(
        self,
        group: str,
        threshold: float,
        mode: Literal["exact", "contains"] = "exact",
        name: str | None = None,
    ) -> None:
        super().__init__(threshold, name or f"Field Accuracy ({group})")
        self.group = group
        self.mode = mode

    def _match(self, actual: Any, expected: Any) -> bool:
        if expected is None:
            return _is_empty(actual)
        if _is_empty(actual):
            return False
        if isinstance(expected, (int, float)) and not isinstance(expected, bool):
            try:
                a = float(actual)
            except (TypeError, ValueError):
                return False
            return abs(a - float(expected)) <= abs(float(expected)) * NUMERIC_TOLERANCE
        a, e = _norm_text(actual), _norm_text(expected)
        if self.mode == "contains":
            return bool(a) and bool(e) and (e in a or a in e)
        return a == e

    def _compute(self, test_case: LLMTestCase) -> tuple[float, str, dict]:
        data = (test_case.metadata or {})[self.group]
        actual: dict = data.get("actual") or {}
        expected: dict = data.get("expected") or {}
        if not expected:
            return 1.0, "No golden fields to compare.", {}
        breakdown = {key: self._match(actual.get(key), value) for key, value in expected.items()}
        misses = [f"{k}: expected {expected[k]!r}, got {actual.get(k)!r}" for k, ok in breakdown.items() if not ok]
        score = sum(breakdown.values()) / len(breakdown)
        reason = "All fields match." if not misses else "Mismatches: " + "; ".join(misses)
        return score, reason, {k: float(v) for k, v in breakdown.items()}


class RankingMetric(_DeterministicMetric):
    """Precision@k, Recall@k or MRR of returned device names against golden relevant names.

    metadata["ranking"] = {"returned": [...], "relevant": [...], "k": int}.
    Precision@k = relevant hits / number of returned items in top k.
    With no relevant devices (negative case) the score is 1.0 only for an empty result.
    """

    LABELS = {"precision_at_k": "Precision@k", "recall_at_k": "Recall@k", "mrr": "MRR"}

    def __init__(
        self,
        kind: Literal["precision_at_k", "recall_at_k", "mrr"],
        threshold: float,
        stage: str,
    ) -> None:
        super().__init__(threshold, f"{self.LABELS[kind]} ({stage})")
        self.kind = kind
        self.stage = stage

    def _compute(self, test_case: LLMTestCase) -> tuple[float, str, dict]:
        data = (test_case.metadata or {})["ranking"]
        k = int(data["k"])
        returned = [_norm_name(n) for n in data["returned"]][:k]
        relevant = {_norm_name(n) for n in data["relevant"]}

        if not relevant:
            score = 1.0 if not returned else 0.0
            return score, f"Negative case: expected no results, got {len(returned)}.", {}

        hits = [name in relevant for name in returned]
        if self.kind == "precision_at_k":
            score = sum(hits) / len(returned) if returned else 0.0
        elif self.kind == "recall_at_k":
            score = sum(hits) / len(relevant)
        else:
            score = next((1.0 / (i + 1) for i, hit in enumerate(hits) if hit), 0.0)
        reason = f"{sum(hits)} of {len(relevant)} relevant in top {k}; returned: {data['returned'][:k]}"
        return score, reason, {"hits": float(sum(hits)), "returned": float(len(returned))}


class FoundDetectionMetric(_DeterministicMetric):
    """Web research must detect whether the device exists; a found device must cite sources.

    metadata["research"] = {"found": bool, "expect_found": bool, "sources": [...]}.
    """

    def __init__(self, threshold: float) -> None:
        super().__init__(threshold, "Found Detection")

    def _compute(self, test_case: LLMTestCase) -> tuple[float, str, dict]:
        data = (test_case.metadata or {})["research"]
        found, expect_found, sources = bool(data["found"]), bool(data["expect_found"]), data.get("sources") or []
        if found != expect_found:
            return 0.0, f"found={found}, expected {expect_found}.", {}
        if found and not sources:
            return 0.0, "Device found but no source URLs were cited.", {}
        return 1.0, f"found={found} as expected, {len(sources)} sources.", {}
