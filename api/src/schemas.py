from types import NoneType
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    template_id: UUID | NoneType
    group_id: List[str] | NoneType
    newsletter_id: UUID
    users_id: List[UUID] | NoneType
    worker_names: List[str]
    subject: str | NoneType
    email_body: str | NoneType


class Messages(BaseModel):
    messages: List[Message]


class QueueMessage(BaseModel):
    email: EmailStr
    subject: str | NoneType
    email_body: str | NoneType
    template_id: UUID | NoneType
    newsletter_id: UUID
    user_id: UUID
    username: str
