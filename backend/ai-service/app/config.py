from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/packman"
    openai_api_key: str = ""
    port: int = 8001
    faiss_index_path: str = "data/faiss_index"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
