from datetime import datetime
from types import NoneType
from typing import List
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


class BaseModelMixin(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads

        def json_dumps(v, *, default):
            return orjson.dumps(v, default=default).decode()


class Message(BaseModelMixin):
    # id: UUID
    type: str
    # transport: str
    # priority: int | NoneType = 0
    # expire_at: datetime
    #
    # x_request_id: str | NoneType
    #
    # users_id: List[UUID]
    # extra: dict = Field(default_factory=dict)
