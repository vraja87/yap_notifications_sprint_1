CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE templates
(
    id               UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    template_name    VARCHAR(255) NOT NULL,
    template_content TEXT         NOT NULL
);

CREATE TABLE schedule
(
    id               UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name             VARCHAR(255) NOT NULL,
    cron_expression  VARCHAR(255) NOT NULL,
    last_update_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    template_id      UUID REFERENCES templates (id) ON DELETE CASCADE,
    worker_names     VARCHAR(255)[] DEFAULT ARRAY['smtp']::VARCHAR(255)[]
);

CREATE TABLE events
(
    id               UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    schedule_id      UUID REFERENCES schedule (id) ON DELETE CASCADE,
    time             TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    status           VARCHAR(20) DEFAULT 'created',
    success_count    INT DEFAULT NULL,
    error_count      INT DEFAULT NULL
);

INSERT INTO templates (id, template_name, template_content)
VALUES
    (uuid_generate_v4(), 'welcome_letter', '<!DOCTYPE html><html><head><title>Welcome</title></head><body><h1>Welcome {{ username }}!</h1><p>Thank you for registering on our platform.</p></body></html>'),
    (uuid_generate_v4(), 'summary_letter', '<!DOCTYPE html><html><head><title>Weekend Movie Summary</title></head><body><h1>Best Movies on This Weekend</h1><p>Here are the top movies you do not want to miss this weekend: {{ movie_list }}</p></body></html>'),
    (uuid_generate_v4(), 'test_letter', '<!DOCTYPE html><html><head><title>Every Minute Task</title></head><body><h1>Task Running Every Minute</h1><p>Current Date and Time: {{ current_datetime }}</p></body></html>'),
    (uuid_generate_v4(), 'likes_summary_letter', '<!DOCTYPE html><html><head><title>Likes Notification</title></head><body><h1>Hi {{ username }}!</h1><p>You have received {{ new_likes }} new likes!<br>Awesome.</p></body></html>');

INSERT INTO schedule (id, name, cron_expression, template_id, worker_names)
VALUES
    (uuid_generate_v4(), 'every_minute_task', '* * * * *', (SELECT id FROM templates WHERE template_name = 'test_letter'), ARRAY['smtp']),
    (uuid_generate_v4(), 'friday_17_00_task', '0 17 * * FRI', (SELECT id FROM templates WHERE template_name = 'summary_letter'), ARRAY['smtp']),
    (uuid_generate_v4(), 'every_day_21_00_task', '0 21 * * *', (SELECT id FROM templates WHERE template_name = 'welcome_letter'), ARRAY['smtp']);
