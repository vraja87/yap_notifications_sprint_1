import os

from pydantic import BaseModel


class DBParams(BaseModel):
    user: str = "notify"
    password: str = "notify"
    host: str = "notify_db"
    port: str = "5432"
    database: str = "notify"


class NotifyAPI(BaseModel):
    url: str = os.getenv("NOTIFY_API")


db_params = DBParams()
notify_api = NotifyAPI()
