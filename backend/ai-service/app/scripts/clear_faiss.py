"""Clear Qdrant vector index data.

Run: uv run packman-clear-faiss
or:  uv run python -m app.scripts.clear_faiss
"""

import sys

from qdrant_client import QdrantClient

from app.config import settings


def main() -> int:
    if settings.qdrant_url:
        client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    else:
        client = QdrantClient(path=settings.qdrant_path)
    collection = settings.qdrant_collection
    try:
        client.delete_collection(collection_name=collection)
        print(f"Deleted Qdrant collection: {collection}")
    except Exception as e:  # noqa: BLE001
        # If the collection doesn't exist, treat as success; otherwise report error.
        message = str(e).lower()
        if "not found" in message or "does not exist" in message:
            print(f"Qdrant collection not found: {collection}")
            return 0
        print(f"Failed to clear Qdrant collection '{collection}': {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
