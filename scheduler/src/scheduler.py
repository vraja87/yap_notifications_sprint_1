import logging
import time

import psycopg
from croniter import croniter

from config import db_params


class CronTaskScheduler:
    def __init__(self):
        self.db_params = db_params.dict()
        self.last_update_time = None

    def execute_task(self, task_name):
        pass

    def fetch_cron_tasks(self):
        logging.error(self.db_params)
        with psycopg.connect(**self.db_params) as conn:
            with conn.cursor() as cursor:

                if self.last_update_time:
                    cursor.execute("SELECT id, task_name, cron_expression FROM cron_tasks WHERE last_update_time > %s", (
                        self.last_update_time,))
                else:
                    cursor.execute("SELECT id, task_name, cron_expression FROM cron_tasks")

                tasks = cursor.fetchall()
                self.last_update_time = time.time()

        return tasks

    def run_tasks(self):
        tasks = self.fetch_cron_tasks()

        for task in tasks:
            logging.error(task)
            task_id, task_name, cron_expression = task
            cron = croniter(cron_expression)

            # Run task if next execution time is less than current time
            if cron.get_next() <= time.time():
                self.execute_task(task_name)

    def start_scheduler(self):
        while True:
            self.run_tasks()
            time.sleep(60)
