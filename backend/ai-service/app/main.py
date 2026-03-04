from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import device as device_api
from app.db.session import engine
from app.db.base import Base
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="PackMan AI Service",
    description="Device description and specifications via OpenAI",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device_api.router, prefix="/api/v1", tags=["device"])


def main() -> None:
  """Entry point for `packman-ai-service` console script."""
  uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)


if __name__ == "__main__":
  main()
