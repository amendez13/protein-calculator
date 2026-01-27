"""Application configuration."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    database_url: str = "sqlite+aiosqlite:///./protein.db"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PROTEIN_", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""

    return Settings()
