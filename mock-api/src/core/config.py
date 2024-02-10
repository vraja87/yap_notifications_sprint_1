from logging import config as logging_config
import os

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = "mock-api"

    db_name: str = os.getenv("NOTIFY_DB_NAME")
    db_user: str = os.getenv("NOTIFY_DB_USER")
    db_password: str = os.getenv("NOTIFY_DB_PASSWORD")
    db_host: str = os.getenv("NOTIFY_DB_HOST")
    db_port: int = 5432
    db_debug: bool = os.getenv("NOTIFY_ENABLE_DEBUG", False)

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()