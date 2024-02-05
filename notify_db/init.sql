CREATE TABLE cron_tasks (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    cron_expression VARCHAR(255) NOT NULL,
    last_update_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO cron_tasks (task_name, cron_expression) VALUES
    ('task1', '0 */12 * * *'),
    ('task2', '30 2 * * *'),
    ('task3', '0 0 * * MON');
