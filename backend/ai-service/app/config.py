from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/packman"
    openai_api_key: str = ""
    port: int = 8001

    # Qdrant: set url to use the server (e.g. Docker dashboard at http://localhost:6333)
    # If unset, uses embedded storage at qdrant_path so no server is required.
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_path: str = "data/qdrant"
    qdrant_collection: str = "devices"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
