import asyncio

from scheduler import CronTaskScheduler

if __name__ == "__main__":
    scheduler = CronTaskScheduler()
    asyncio.run(scheduler.start_scheduler())
