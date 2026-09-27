"""Re-index all devices in Qdrant with the current indexing pipeline.

Reads every point, removes duplicates by name, saves a JSON backup,
recreates the collection and indexes each device again (2 OpenAI calls per device, plus a web search when the device has no description).

Run: uv run packman-reindex-devices
"""

import json
import sys
from pathlib import Path

from app.config import settings
from app.services.device_service import device_service
from app.services.vector_store import vector_store_service

BACKUP_PATH = Path("data/reindex_backup.json")


def load_devices() -> list[dict]:
    client = vector_store_service.client
    devices: dict[str, dict] = {}
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=settings.qdrant_collection,
            limit=256,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for point in points:
            meta = (point.payload or {}).get("metadata") or {}
            name = (meta.get("name") or "").strip()
            if not name:
                continue
            key = name.lower()
            current = devices.get(key)
            if current is None or (not current["description"] and meta.get("description")):
                devices[key] = {
                    "name": name,
                    "price": meta.get("price"),
                    "description": meta.get("description") or "",
                }
        if offset is None:
            break
    return list(devices.values())


def main() -> int:
    devices = load_devices()
    if not devices:
        print("No devices found in Qdrant.")
        return 0

    BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
    BACKUP_PATH.write_text(json.dumps(devices, ensure_ascii=False, indent=2))
    print(f"Found {len(devices)} unique devices. Backup: {BACKUP_PATH}")

    vector_store_service.client.delete_collection(collection_name=settings.qdrant_collection)
    vector_store_service._vectorstore = None

    failed: list[str] = []
    for index, device in enumerate(devices, start=1):
        name = device["name"]
        try:
            description, sources = device_service.resolve_description(name, device["description"])
            specs = device_service.get_device_specs_by_name(name=name, description=description)
            short_description = device_service.get_short_description(
                name, description, device["price"], specs=specs
            )
            vector_store_service.add_device(
                name=name,
                short_description=short_description,
                price=device["price"],
                description=description,
                sources=sources,
                traits=specs.traits,
                specifications=specs.specifications,
                key_features=specs.key_features,
            )
            print(f"[{index}/{len(devices)}] {name}")
        except Exception as error:  # noqa: BLE001
            failed.append(name)
            print(f"[{index}/{len(devices)}] {name} FAILED: {error}", file=sys.stderr)

    if failed:
        print(f"Failed: {len(failed)}. Devices are kept in {BACKUP_PATH}.", file=sys.stderr)
        return 1
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
