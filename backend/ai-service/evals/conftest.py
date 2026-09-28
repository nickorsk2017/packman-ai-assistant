"""DeepEval suite setup: isolated Qdrant collection, seeded golden catalog, summary report."""

import json
import os
import time
from datetime import datetime

import pytest

from app.config import settings

from evals.config import PRODUCTION_COLLECTION, REPORTS_DIR

# Isolation: point the vector store at the eval collection before any service touches Qdrant.
settings.qdrant_collection = settings.eval_qdrant_collection
if not settings.qdrant_url:
    settings.qdrant_path = settings.eval_qdrant_path
if settings.qdrant_collection == PRODUCTION_COLLECTION:
    raise pytest.UsageError(
        f"EVAL_QDRANT_COLLECTION must not be {PRODUCTION_COLLECTION!r}: evals would overwrite production data"
    )

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")

from app.schemas.device import DeviceTraitsAndSpecifications  # noqa: E402
from app.services.device_service import device_service  # noqa: E402
from app.services.vector_store import vector_store_service  # noqa: E402

from evals import collector  # noqa: E402
from evals.datasets import catalog, catalog_device  # noqa: E402


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "add_device: Add Device pipeline evals")
    config.addinivalue_line("markers", "search: Search pipeline evals")


class CatalogOutputs:
    """Runs the Add Device pipeline once per catalog device and caches the result."""

    def __init__(self) -> None:
        self._cache: dict[str, dict] = {}

    def get(self, name: str) -> dict:
        if name not in self._cache:
            device = catalog_device(name)
            with collector.timed("add_device", "specs", name):
                specs: DeviceTraitsAndSpecifications = device_service.get_device_specs_by_name(
                    name=device.name, description=device.description
                )
            with collector.timed("add_device", "short_description", name):
                short_description = device_service.get_short_description(
                    device.name, device.description, device.price, specs=specs
                )
            self._cache[name] = {"specs": specs, "short_description": short_description}
        return self._cache[name]


@pytest.fixture(scope="session")
def catalog_outputs() -> CatalogOutputs:
    return CatalogOutputs()


@pytest.fixture(scope="session")
def seeded_index(catalog_outputs: CatalogOutputs) -> str:
    """Drop and re-seed the eval collection with the golden catalog through the real pipeline."""
    name = settings.qdrant_collection
    assert name != PRODUCTION_COLLECTION
    client = vector_store_service.client
    if client.collection_exists(name):
        client.delete_collection(name)
    vector_store_service._vectorstore = None

    for device in catalog():
        out = catalog_outputs.get(device.name)
        specs: DeviceTraitsAndSpecifications = out["specs"]
        vector_store_service.add_device(
            name=device.name,
            short_description=out["short_description"],
            price=device.price,
            description=device.description,
            sources=[],
            traits=specs.traits,
            specifications=specs.specifications,
            key_features=specs.key_features,
        )
    return name


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not collector.RESULTS:
        return
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "judge_model": settings.eval_judge_model,
        "qdrant_collection": settings.qdrant_collection,
        **collector.summary(),
        "results": collector.RESULTS,
        "latencies": collector.LATENCIES,
    }
    path = REPORTS_DIR / f"summary-{time.strftime('%Y%m%d-%H%M%S')}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    session.config._eval_report_path = str(path)  # type: ignore[attr-defined]


def pytest_terminal_summary(terminalreporter, exitstatus: int, config: pytest.Config) -> None:
    if not collector.RESULTS:
        return
    data = collector.summary()
    tr = terminalreporter
    tr.section("DeepEval metrics summary")
    tr.write_line(f"{'pipeline':<11} {'stage':<18} {'metric':<40} {'n':>3} {'mean':>6} {'pass':>6} {'thr':>5}")
    for m in data["metrics"]:
        mean_score = "-" if m["mean_score"] is None else f"{m['mean_score']:.2f}"
        tr.write_line(
            f"{m['pipeline']:<11} {m['stage']:<18} {m['metric'][:40]:<40} {m['n']:>3} "
            f"{mean_score:>6} {m['pass_rate']:>6.0%} {m['threshold']:>5}"
        )
    tr.write_line("")
    for lat in data["latency"]:
        tr.write_line(f"latency {lat['pipeline']}/{lat['stage']}: mean {lat['mean_seconds']}s, max {lat['max_seconds']}s")
    tr.write_line(f"judge cost: ${data['judge_cost_usd']}")
    path = getattr(config, "_eval_report_path", None)
    if path:
        tr.write_line(f"report: {path}")
