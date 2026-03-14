"""Run Qdrant server (Docker) with web dashboard.

Usage:
  uv run packman-run-qdrant

Dashboard: http://localhost:6333/dashboard
API: http://localhost:6333
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    # Directory containing docker-compose.yml (backend/ai-service)
    root = Path(__file__).resolve().parent.parent.parent
    compose_dir = root
    compose_file = compose_dir / "docker-compose.yml"
    if not compose_file.exists():
        print(f"docker-compose.yml not found at {compose_file}", file=sys.stderr)
        return 1
    if not shutil.which("docker"):
        print("Docker is not installed or not in PATH. Install Docker and try again.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=compose_dir,
        env=env,
    )
    if result.returncode == 0:
        print("Qdrant server starting. Dashboard: http://localhost:6333/dashboard")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
