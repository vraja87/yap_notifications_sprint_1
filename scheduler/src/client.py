from typing import List

from loguru import logger
import httpx

from config import notify_api


class NotifyAPIClient:
    def __init__(self):
        self.notify = f"{notify_api.url}publish/"

    async def send_schedule_data(
        self,
        newsletter_id: int,
        template_id: int,
        group_id: List[int] = None,
        worker_names: List[str] = None,
        user_id: List[int] = None,
    ) -> None:

        data = {
            "template_id": template_id,
            "group_id": group_id,
            "newsletter_id": newsletter_id,
            "user_id": user_id,
            "worker_names": worker_names,
        }

        logger.info(data)

        async with httpx.AsyncClient() as client:
            logger.error(self.notify)
            response = await client.post(self.notify, json=data)

        if response.status_code == 200:
            logger.info("Data sent successfully!")
        else:
            logger.info(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")
