"""Clear FAISS vector index data. Run: uv run python -m app.scripts.clear_faiss"""

import shutil
import sys
from pathlib import Path

from app.config import settings


def main() -> int:
    target = Path(settings.faiss_index_path).resolve()
    if not target.exists():
        print(f"FAISS index path does not exist: {target}")
        return 0
    try:
        if target.is_dir():
            shutil.rmtree(target)
            print(f"Removed FAISS index directory: {target}")
        else:
            target.unlink()
            print(f"Removed FAISS index file: {target}")
    except OSError as e:
        print(f"Failed to clear FAISS data: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
