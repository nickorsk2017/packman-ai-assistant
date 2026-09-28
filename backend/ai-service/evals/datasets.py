"""Typed loaders for the golden datasets in evals/datasets."""

import json
from functools import lru_cache
from typing import Any

from pydantic import BaseModel

from evals.config import DATASETS_DIR


class CatalogDevice(BaseModel):
    name: str
    price: float
    description: str
    traits: dict[str, Any]
    specifications: dict[str, Any]


class ResearchCase(BaseModel):
    name: str
    expect_found: bool
    reference: str = ""
    key_facts: list[str] = []


class SearchCase(BaseModel):
    id: str
    prompt: str
    k: int = 5
    max_price: float | None = None
    traits: dict[str, Any]
    relevant: list[str]


def _load(file_name: str) -> dict:
    with open(DATASETS_DIR / file_name, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def catalog() -> list[CatalogDevice]:
    return [CatalogDevice.model_validate(d) for d in _load("devices_catalog.json")["devices"]]


def catalog_device(name: str) -> CatalogDevice:
    for device in catalog():
        if device.name == name:
            return device
    raise KeyError(f"Device {name!r} is not in devices_catalog.json")


@lru_cache(maxsize=1)
def research_cases() -> list[ResearchCase]:
    return [ResearchCase.model_validate(c) for c in _load("add_device_cases.json")["research"]]


@lru_cache(maxsize=1)
def description_devices() -> list[str]:
    return list(_load("add_device_cases.json")["description_devices"])


@lru_cache(maxsize=1)
def search_cases() -> list[SearchCase]:
    return [SearchCase.model_validate(c) for c in _load("search_cases.json")["cases"]]
