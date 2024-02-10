import asyncio
from loguru import logger
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import db_params

class CronTaskScheduler:
    def __init__(self):
        self.db_params = db_params.dict()
        self.scheduler = AsyncIOScheduler()

    async def execute_task(self, task_id, task_name):
        logger.info(f"Executing task {task_name} with ID: {task_id}")
        await asyncio.sleep(2)
        logger.info(f"End executing task {task_name} with ID: {task_id}")

    async def fetch_cron_tasks(self) -> list:
        logger.info("Fetching cron tasks from database...")
        tasks = []

        async with asyncpg.create_pool(**self.db_params) as pool:
            async with pool.acquire() as conn:
                tasks = await conn.fetch("SELECT id, task_name, cron_expression FROM schedule")

        logger.info(f"Found {len(tasks)} cron tasks.")
        return tasks

    async def schedule_tasks(self) -> None:
        tasks = await self.fetch_cron_tasks()

        for task in tasks:
            task_id, task_name, cron_expression = task
            logger.info(f"Scheduling task {task_name} with cron expression: {cron_expression}")

            trigger = CronTrigger.from_crontab(cron_expression)
            self.scheduler.add_job(func=self.execute_task, trigger=trigger, args=[task_id, task_name], id=f"task_{task_id}")

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