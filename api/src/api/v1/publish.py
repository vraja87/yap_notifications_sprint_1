from fastapi import APIRouter, status

from producer import producer
from schemas import Message

router = APIRouter()


@router.post("/publish/", status_code=status.HTTP_200_OK)
async def publish(message: Message):
    return await producer.publish(message=message.dict())
