"""Search pipeline: trait extraction from the prompt, vector retrieval, LLM rerank.

Reproduces the orchestration of GET /device/search against the isolated eval collection.
"""

import json

import pytest
from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric
from deepeval.test_case import LLMTestCase

from app.api.device import SEARCH_CANDIDATES_MAX, SEARCH_CANDIDATES_MULTIPLIER
from app.services.device_service import device_service
from app.services.vector_store import build_page_content, vector_store_service

from evals import collector
from evals.config import threshold
from evals.datasets import SearchCase, search_cases
from evals.judge import judge_model
from evals.metrics import FieldAccuracyMetric, RankingMetric

pytestmark = pytest.mark.search

PIPELINE = "search"
NO_RESULTS = "No devices returned."

_RUNS: dict[str, dict] = {}


def run_search(case: SearchCase) -> dict:
    """Run the search flow once per case and cache every stage output."""
    if case.id in _RUNS:
        return _RUNS[case.id]
    with collector.timed(PIPELINE, "traits", case.id):
        traits = device_service.get_specifications_by_user_prompt(user_prompt=case.prompt)
    with collector.timed(PIPELINE, "retrieval", case.id):
        candidates = vector_store_service.search(
            case.prompt,
            k=min(case.k * SEARCH_CANDIDATES_MULTIPLIER, SEARCH_CANDIDATES_MAX),
            max_price=case.max_price or traits.price or None,
            traits=traits,
        )
    with collector.timed(PIPELINE, "rerank", case.id):
        reranked = device_service.rerank_devices(case.prompt, candidates)[: case.k]
    _RUNS[case.id] = {
        "traits": traits,
        "retrieval": candidates[: case.k],
        "rerank": reranked,
    }
    return _RUNS[case.id]


def page_text(device: dict) -> str:
    return build_page_content(
        device.get("name", ""),
        device.get("short_description") or "",
        device.get("traits") or {},
        device.get("specifications") or {},
        device.get("key_features") or [],
    )


@pytest.mark.parametrize("case", search_cases(), ids=lambda c: c.id)
def test_trait_extraction(case: SearchCase, seeded_index: str) -> None:
    traits = run_search(case)["traits"]
    actual = traits.model_dump()
    test_case = LLMTestCase(
        input=case.prompt,
        actual_output=json.dumps(traits.model_dump(exclude_none=True), ensure_ascii=False),
        metadata={"traits": {"actual": actual, "expected": case.traits}},
    )
    metrics = [FieldAccuracyMetric("traits", threshold=threshold("search_traits_accuracy"), mode="exact")]
    collector.evaluate(test_case, metrics, pipeline=PIPELINE, stage="traits", case_id=case.id)


@pytest.mark.parametrize("stage", ["retrieval", "rerank"])
@pytest.mark.parametrize("case", search_cases(), ids=lambda c: c.id)
def test_ranking(case: SearchCase, stage: str, seeded_index: str) -> None:
    negative = not case.relevant
    if negative and stage == "retrieval":
        pytest.skip("Vector retrieval always returns nearest neighbours; negatives are judged after rerank.")

    devices = run_search(case)[stage]
    names = [d.get("name", "") for d in devices]
    metrics = [
        RankingMetric("precision_at_k", threshold(f"{stage}_precision_at_k"), stage),
        RankingMetric("recall_at_k", threshold(f"{stage}_recall_at_k"), stage),
        RankingMetric("mrr", threshold(f"{stage}_mrr"), stage),
    ]
    expected_output = None
    if not negative:
        expected_output = "The best matching devices for this request are: " + "; ".join(case.relevant) + "."
        metrics += [
            ContextualPrecisionMetric(threshold=threshold(f"{stage}_contextual_precision"), model=judge_model()),
            ContextualRecallMetric(threshold=threshold(f"{stage}_contextual_recall"), model=judge_model()),
            ContextualRelevancyMetric(threshold=threshold(f"{stage}_contextual_relevancy"), model=judge_model()),
        ]

    test_case = LLMTestCase(
        input=case.prompt,
        actual_output="; ".join(names) or NO_RESULTS,
        expected_output=expected_output,
        retrieval_context=[page_text(d) for d in devices] or [NO_RESULTS],
        metadata={"ranking": {"returned": names, "relevant": case.relevant, "k": case.k}},
    )
    collector.evaluate(test_case, metrics, pipeline=PIPELINE, stage=stage, case_id=case.id)
