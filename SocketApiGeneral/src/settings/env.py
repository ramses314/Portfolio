from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    cors_allowed_origins: List[str]

    model_config = ConfigDict(extra="ignore")


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str

    model_config = ConfigDict(extra="ignore")


database_settings = DatabaseSettings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
core_settings = CoreSettings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)

database_url = (
    f"postgresql+asyncpg://{database_settings.db_user}:"
    f"{database_settings.db_pass}@{database_settings.db_host}:"
    f"{database_settings.db_port}/{database_settings.db_name}"
)
