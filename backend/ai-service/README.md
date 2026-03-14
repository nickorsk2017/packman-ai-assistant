# PackMan AI Service

Device descriptions, tags, and vector search (Qdrant).

## Setup

```bash
uv sync
```

## Run the service

```bash
uv run packman-ai-service
```

## Qdrant client & dashboard

- **Python client**: `qdrant-client` is already in dependencies (see `pyproject.toml`). Install with `uv sync`.
- **Why the dashboard shows no collections**: The app can use either **embedded** storage (`data/qdrant`) or a **Qdrant server** (Docker). Embedded storage uses a different format; the server dashboard cannot read it, so the collection list stays empty until you use the server.

- **To see the collection list in the dashboard** (e.g. http://localhost:6333/dashboard#/collections):

  1. **Start the Qdrant server** (before the AI service):
     ```bash
     uv run packman-run-qdrant
     ```
     Or: `docker compose up -d`

  2. **Point the app at the server** — in `.env` add:
     ```env
     QDRANT_URL=http://localhost:6333
     ```

  3. **Restart the AI service** and **index a device** from the app (e.g. Add Device on the search page). The `devices` collection will be created on the server and will appear in the dashboard.

  Then open:

  - **Dashboard**: http://localhost:6333/dashboard  
  - **REST API**: http://localhost:6333  

  Without `QDRANT_URL`, the app uses embedded storage at `data/qdrant`; that data is not visible in the server dashboard.

  Stop the server:

  ```bash
  docker compose down
  ```
