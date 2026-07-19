from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    log_level: str = "INFO"
    app_version: str = "dev"


@lru_cache
def get_settings() -> Settings:
    return Settings()
