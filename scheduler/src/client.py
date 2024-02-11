import json
import uuid
from typing import List

from loguru import logger
import httpx

from config import notify_api


class NotifyAPIClient:
    def __init__(self):
        self.notify = f"{notify_api.url}publish/"

    async def send_schedule_data(
        self,
        newsletter_id: uuid.UUID,
        template_id: uuid.UUID,
        group_id: List[str] = None,
        worker_names: List[str] = None,
        user_id: List[uuid.UUID] = None,
    ) -> None:
        uuid_str_list = [str(u_uuid) for u_uuid in user_id]
        json_uuid_list = json.dumps(uuid_str_list)

        data = {
            "messages": [
                {
                    "template_id": str(template_id),
                    "group_id": group_id,
                    "newsletter_id": str(newsletter_id),
                    "user_id": json_uuid_list,
                    "worker_names": worker_names,
                }
            ]
        }

        async with httpx.AsyncClient() as client:
            logger.error(self.notify)
            response = await client.post(self.notify, json=data)

        if response.status_code == 200:
            logger.info("Data sent successfully!")
        else:
            logger.info(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")
