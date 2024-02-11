import asyncio

from loguru import logger
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from client import NotifyAPIClient
from config import db_params


class CronTaskScheduler:
    def __init__(self):
        self.db_params = db_params.dict()
        self.scheduler = AsyncIOScheduler()
        self.api_client = NotifyAPIClient()

    async def execute_task(self, schedule_id, schedule_name, template_id):
        logger.info(f"Executing task {schedule_name} with ID: {schedule_id}")

        event_id = await self.create_event(schedule_id)

        await self.api_client.send_schedule_data(
            template_id=template_id,
            group_id=[1, 2, 3],
            newsletter_id=123,
            users_id=[456, 789],
            worker_names=["worker1", "worker2"],
        )
        logger.info(f"End executing task {schedule_name}. Stored event_id: {event_id}")

    async def create_event(self, schedule_id) -> int | None:
        logger.info("Inserting event to database...")

        async with asyncpg.create_pool(**self.db_params) as pool:
            async with pool.acquire() as conn:
                query = "INSERT INTO events (schedule_id, status) VALUES ($1, $2) RETURNING id"
                values = (schedule_id, "created")
                result = await conn.fetchrow(query, *values)
                logger.info(f"Event inserted with ID: {result['id']}")
                return result["id"]

    async def fetch_cron_tasks(self) -> list:
        logger.info("Fetching cron tasks from database...")
        tasks = []

        async with asyncpg.create_pool(**self.db_params) as pool:
            async with pool.acquire() as conn:
                tasks = await conn.fetch("SELECT id, name, cron_expression, template_id FROM schedule")

        logger.info(f"Found {len(tasks)} cron tasks.")
        return tasks

    async def schedule_tasks(self) -> None:
        tasks = await self.fetch_cron_tasks()

        for task in tasks:
            schedule_id, schedule_name, cron_expression, template_id = task
            logger.info(f"Scheduling task {schedule_name} with cron expression: {cron_expression}")
            trigger = CronTrigger.from_crontab(cron_expression)
            self.scheduler.add_job(
                func=self.execute_task, trigger=trigger, args=[schedule_id, schedule_name, template_id]
            )

    async def start_scheduler(self) -> None:
        logger.info("Starting scheduler.")
        try:
            await self.schedule_tasks()
            self.scheduler.start()

            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by the user.")
        except Exception as e:
            logger.exception("An error occurred in the scheduler.", exc_info=True)
        finally:
            # Stop the scheduler
            self.scheduler.shutdown(wait=False)
