"""Settings."""

from functools import lru_cache

from pydantic import MongoDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    app_name: str
    app_version: str = '0.1.0'
    app_doc_url: str = '/docs'
    app_description: str = ''
    debug: bool = False

    # MongoDB
    mongodb_url: MongoDsn
    mongodb_db_name: str

    # MQTT
    mqtt_host: str = 'localhost'
    mqtt_port: int = 1883
    mqtt_username: str = 'admin'
    mqtt_password: SecretStr = SecretStr('public')
    mqtt_timeout: float | None = 3.5
    mqtt_qos: int = 2
    mqtt_topic_prefix: str


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
