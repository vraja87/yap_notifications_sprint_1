from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path("../..") / ".env"
env_file = env_path


class DBParams(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file)
    user: str = Field("notify", env="NOTIFY_DB_USER")
    password: str = Field("notify", env="NOTIFY_DB_PASSWORD")
    host: str = Field("notify_db", env="NOTIFY_DB_HOST")
    port: str = Field("5432", env="NOTIFY_DB_PORT")
    database: str = Field("notify", env="NOTIFY_DB_NAME")


class NotifyAPI(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file)
    url: str = Field("http://api:8000/api/v1/", env="NOTIFY_API")


# TODO: any options to work without env file - just with env vars? it workerd on old v1 pydantic...

db_params = DBParams()
notify_api = NotifyAPI()
