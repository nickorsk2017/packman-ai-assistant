"""Add Device pipeline: web research, traits/specifications extraction, short description."""

import json

import pytest
from deepeval.metrics import FaithfulnessMetric, GEval, HallucinationMetric
from deepeval.test_case import LLMTestCase, SingleTurnParams

from app.services.device_service import device_service

from evals import collector
from evals.config import threshold
from evals.datasets import ResearchCase, catalog, catalog_device, description_devices, research_cases
from evals.judge import judge_model
from evals.metrics import FieldAccuracyMetric, FoundDetectionMetric

pytestmark = pytest.mark.add_device

PIPELINE = "add_device"


# ---------- web research ----------

@pytest.mark.parametrize("case", research_cases(), ids=lambda c: c.name)
def test_research(case: ResearchCase) -> None:
    with collector.timed(PIPELINE, "research", case.name):
        research = device_service.research_device(case.name)

    metrics = [FoundDetectionMetric(threshold=threshold("research_found"))]
    expected_output = None
    context = None
    if case.expect_found and research.found:
        expected_output = case.reference + "\nKey facts: " + "; ".join(case.key_facts)
        context = [case.reference]
        metrics += [
            HallucinationMetric(threshold=threshold("hallucination"), model=judge_model()),
            GEval(
                name="Research Correctness",
                criteria=(
                    "Check that every specification in the actual output (display, processor, RAM, storage, "
                    "cameras, battery, OS, release date, price) agrees with the expected output. Penalize specs "
                    "that belong to a different model or contradict the expected output. Facts missing from the "
                    "expected output are not errors unless they are clearly wrong."
                ),
                evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
                threshold=threshold("research_correctness"),
                model=judge_model(),
            ),
            GEval(
                name="Research Completeness",
                criteria=(
                    "Check how many of the 'Key facts' listed in the expected output are present in the actual "
                    "output. Score is the share of key facts covered."
                ),
                evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
                threshold=threshold("research_completeness"),
                model=judge_model(),
            ),
        ]

    test_case = LLMTestCase(
        input=case.name,
        actual_output=research.facts or "FOUND: no",
        expected_output=expected_output,
        context=context,
        metadata={
            "research": {"found": research.found, "expect_found": case.expect_found, "sources": research.sources},
        },
    )
    collector.evaluate(test_case, metrics, pipeline=PIPELINE, stage="research", case_id=case.name)


# ---------- traits + specifications extraction ----------

@pytest.mark.parametrize("device", catalog(), ids=lambda d: d.name)
def test_specs_extraction(device, catalog_outputs) -> None:
    specs = catalog_outputs.get(device.name)["specs"]
    traits = specs.traits.model_dump() if specs.traits else {}
    specifications = specs.specifications.model_dump() if specs.specifications else {}

    test_case = LLMTestCase(
        input=f"{device.name}\n\nSeller description: {device.description}",
        actual_output=json.dumps(specs.model_dump(exclude_none=True), ensure_ascii=False),
        metadata={
            "traits": {"actual": traits, "expected": device.traits},
            "specifications": {"actual": specifications, "expected": device.specifications},
        },
    )
    metrics = [
        FieldAccuracyMetric("traits", threshold=threshold("specs_traits_accuracy"), mode="exact"),
        FieldAccuracyMetric(
            "specifications", threshold=threshold("specs_specifications_accuracy"), mode="contains"
        ),
    ]
    collector.evaluate(test_case, metrics, pipeline=PIPELINE, stage="specs", case_id=device.name)


# ---------- short description ----------

@pytest.mark.parametrize("name", description_devices())
def test_short_description(name: str, catalog_outputs) -> None:
    device = catalog_device(name)
    out = catalog_outputs.get(name)
    specs = out["specs"]

    retrieval_context = [
        f"Seller description: {device.description}",
        f"Extracted specifications: {json.dumps(specs.model_dump(exclude_none=True), ensure_ascii=False)}",
        f"Seller price: {device.price} USD",
    ]
    test_case = LLMTestCase(
        input=device.name,
        actual_output=out["short_description"],
        retrieval_context=retrieval_context,
    )
    display_count = specs.traits.display_count if specs.traits else None
    metrics = [
        FaithfulnessMetric(threshold=threshold("faithfulness"), model=judge_model()),
        GEval(
            name="Description Quality",
            evaluation_steps=[
                "The actual output is an HTML snippet using only H1, P and B tags.",
                "It is 3-5 sentences of plain consumer language and does not list raw specifications.",
                "It explains what the device is good for and which type of user it fits.",
                "It does not state the device name (input).",
                "It uses only facts present in the retrieval context and adds no invented features.",
                (
                    "The device has two screens, so the second screen must be named as a main strength."
                    if display_count and display_count >= 2
                    else "Ignore screen count."
                ),
            ],
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.RETRIEVAL_CONTEXT,
            ],
            threshold=threshold("description_quality"),
            model=judge_model(),
        ),
    ]
    collector.evaluate(test_case, metrics, pipeline=PIPELINE, stage="short_description", case_id=name)
