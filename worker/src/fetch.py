from datetime import datetime

import aiohttp
from loguru import logger
from src.config import conf_service, config_notify_db, settings
from src.connector.postgres import PostgresConnector
from src.models.models import ContentSummary, Movie, TemplateModel, UGCSummary


async def fetch_ugc_summary(user_id: str, since: datetime) -> UGCSummary:
    since_formatted = since.isoformat()
    url = f"http://mock-api/ugc/v1/summary?user_id={user_id}&since={since_formatted}"
    headers = {
        'Cookie': f'access_token={conf_service.token}; HttpOnly; Path=/',
        "X-Request-Id": settings.mock_x_request_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_likes = await response.json()
                return await UGCSummary(**response_likes)
            else:
                raise Exception(f'Failed to fetch UGC summary, status code: {response.status}')


async def fetch_content_summary(user_id: str) -> ContentSummary:
    url = f"http://mock-api/content/v1/summary?user_id={user_id}"
    headers = {
        'Cookie': f'access_token={conf_service.token}; HttpOnly; Path=/',
        "X-Request-Id": settings.mock_x_request_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_content = await response.json()
                return ContentSummary(movies=[Movie(**movie) for movie in response_content])
            else:
                raise Exception(f'Failed to fetch content summary, status code: {response.status}')


@logger.catch
async def fetch_template_by_id(template_id: str) -> TemplateModel:
    connector = PostgresConnector(dsn=config_notify_db.dsn)
    await connector.connect()

    try:
        query = "SELECT template_name, template_content FROM templates WHERE id = $1"
        template_data = await connector.fetch(query, template_id)
        if template_data:
            return TemplateModel(**template_data[0])
        else:
            raise Exception(f"Template not found. id: {template_id}")
    finally:
        await connector.close()
