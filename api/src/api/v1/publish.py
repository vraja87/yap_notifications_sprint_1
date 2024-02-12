import os
import httpx
import orjson

from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends, BackgroundTasks

from producer import get_producer, QueueProducer
from cache import get_cache, Cache
from core.config import settings
from schemas import Messages, QueueMessage, Message

router = APIRouter()


async def send_messages(
    queue_producer: QueueProducer,
    cache: Cache,
    data,
    immediate=False,
):
    cache_key = "users"
    if getattr(data, "group_id", None):
        group_id = [str(i) for i in data.group_id]
        group_id.sort()
        filter = f'?group_id={"&group_id=".join(group_id)}'
        url = f"/auth/v1/users/users_by_group{filter}"
        cache_key = f"{cache_key}_{','.join(group_id)}"
    else:
        url = "/auth/v1/users?"
    messages = await cache.get(cache_key)
    update_time = await cache.get(f"{cache_key}_update_time")

    if update_time:
        update_time = datetime.strptime(update_time["time"], "%m/%d/%Y, %H:%M:%S")

    # if there is no cache present
    if (not update_time or datetime.now() - update_time > timedelta(days=1)
            or not messages):
        async with httpx.AsyncClient(base_url=settings.auth_api_url) as client:
            headers = {
                "Cookie": f'''access_token={
                    os.environ.get('SERVICE_TOKEN')}; HttpOnly; Path=/''',
                "X-Request-Id": "ServiceForGatheringData"
                }
            s = await client.get(
                url,
                headers=headers)
            messages = s.json()["items"]
            for i in range(1, s.json()["pages"]):
                s = await client.get(
                    f"{url}&page={i}",
                    headers=headers)
                messages += s.json()["items"]
            r = await cache.set(cache_key, orjson.dumps(messages), 60*60*24)
            if r:
                r = await cache.set(
                    f"{cache_key}_update_time",
                    orjson.dumps({"time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}),
                    60*60*24)
    for worker in data.worker_names:
        for i in messages:
            await queue_producer.publish(
                message=QueueMessage(
                    email=i["email"],
                    subject=getattr(data, "subject", None),
                    email_body=getattr(data, "email_body", None),
                    template_id=getattr(data, "template_id", None),
                    newsletter_id=getattr(data, "newsletter_id", None),
                    user_id=i["id"],
                    username=i["login"],
                ),
                routing_key=f'''{worker}.{
                    settings.IMMEDIATE_QUEUE_NAME if immediate else settings.QUEUE_NAME}''')


@router.post("/publish/", status_code=status.HTTP_201_CREATED)
async def publish(
    data: Messages,
    background_tasks: BackgroundTasks,
    queue_producer: QueueProducer = Depends(get_producer),
    cache: Cache = Depends(get_cache),
):
    for i in data.messages:
        background_tasks.add_task(send_messages, queue_producer, cache, i)


@router.post("/publish_immediate/", status_code=status.HTTP_201_CREATED)
async def publish_immediate(
    data: Messages,
    background_tasks: BackgroundTasks,
    queue_producer: QueueProducer = Depends(get_producer),
    cache: Cache = Depends(get_cache),
):
    for i in data.messages:
        background_tasks.add_task(
            send_messages,
            queue_producer,
            cache,
            i,
            True
        )



@router.get("/consume/", status_code=status.HTTP_201_CREATED)
async def consume(queue_producer: QueueProducer = Depends(get_producer)):
    res = await queue_producer.channel.declare_queue(
        settings.QUEUE_NAME, durable=True, arguments={"x-max-priority": 10})
    return {"Count": res.declaration_result.message_count}
