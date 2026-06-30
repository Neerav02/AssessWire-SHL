from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    app_env: str = "local"
    catalog_path: Path = Path("data/catalog/catalog_clean.json")
    max_recommendations: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

