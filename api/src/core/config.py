import os
from pathlib import Path

from pydantic import BaseSettings, Field

env_path = Path("..") / ".env"
env_file = env_path


class Settings(BaseSettings):
    PROJECT_NAME: str = "NOTIFICATIONS"
    PRODUCER_DSN: str = Field(env="RABBITMQ_URI")
    QUEUE_NAME: str = Field("notice", env="QUEUE_NAME")
    IMMEDIATE_QUEUE_NAME: str = Field("notice", env="IMMEDIATE_QUEUE_NAME")

    service_token: str = os.getenv("SERVICE_TOKEN")

    redis_host: str = os.getenv("CACHE_HOST")
    redis_port: int = os.getenv("CACHE_PORT")


settings = Settings()
