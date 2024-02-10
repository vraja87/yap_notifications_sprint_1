import asyncio
from scheduler import CronTaskScheduler

async def main():
    scheduler = CronTaskScheduler()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        await scheduler.start_scheduler()
    finally:
        loop.close()

if __name__ == "__main__":
    asyncio.run(main())
