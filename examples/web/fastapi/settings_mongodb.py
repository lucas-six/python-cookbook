"""Settings with MongoDB."""

from functools import lru_cache

from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    app_name: str
    app_version: str = '0.1.0'
    app_doc_url: str = '/docs'
    app_description: str = ''
    debug: bool = False
    mongodb_url: MongoDsn
    mongodb_db_name: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
