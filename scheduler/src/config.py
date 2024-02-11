import os

from pydantic import BaseModel


class DBParams(BaseModel):
    user: str = os.getenv("NOTIFY_DB_USER")
    password: str = os.getenv("NOTIFY_DB_PASSWORD")
    host: str = os.getenv("NOTIFY_DB_HOST")
    port: str = os.getenv("NOTIFY_DB_PORT")
    database: str = os.getenv("NOTIFY_DB_NAME")


class NotifyAPI(BaseModel):
    url: str = os.getenv("NOTIFY_API")


db_params = DBParams()
notify_api = NotifyAPI()
