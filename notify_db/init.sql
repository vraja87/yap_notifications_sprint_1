CREATE TABLE templates
(
    id               SERIAL PRIMARY KEY,
    template_name    VARCHAR(255) NOT NULL,
    template_content TEXT         NOT NULL
);


CREATE TABLE schedule
(
    id               SERIAL PRIMARY KEY,
    task_name        VARCHAR(255) NOT NULL,
    cron_expression  VARCHAR(255) NOT NULL,
    last_update_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    template_id      INT REFERENCES templates (id) ON DELETE CASCADE
);


INSERT INTO templates (id, template_name, template_content)
VALUES (1, 'welcome_letter',
        '<!DOCTYPE html><html><head><title>Welcome</title></head><body><h1>Welcome {{ username }}!</h1><p>Thank you for registering on our platform.</p></body></html>'),
       (2, 'summary_letter',
        '<!DOCTYPE html><html><head><title>Weekend Movie Summary</title></head><body><h1>Best Movies on This Weekend</h1><p>Here are the top movies you do not want to miss this weekend: {{ movie_list }}</p></body></html>'),
       (3, 'test_letter',
        '<!DOCTYPE html><html><head><title>Every Minute Task</title></head><body><h1>Task Running Every Minute</h1><p>Current Date and Time: {{ current_datetime }}</p></body></html>');


INSERT INTO schedule (task_name, cron_expression, template_id)
VALUES ('every_minute_task', '* * * * *', 3),
       ('friday_17_00_task', '0 17 * * FRI', 2),
       ('every_day_21_00_task', '0 21 * * *', 1);

