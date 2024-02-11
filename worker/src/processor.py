import asyncio
import json
from datetime import datetime, timedelta

import aio_pika
from bs4 import BeautifulSoup
from jinja2 import Template
from loguru import logger
from src.config import config_rabbit, settings
from src.connector.rabbit import RabbitMQ
from src.fetch import (fetch_content_summary, fetch_template_by_id,
                       fetch_ugc_summary)
from src.sender.mail import MailNotification


async def processor_with_templating(message_data):
    """Жёстко темплэйтим типы поддерживаемых писем. Затем запускает простой обработчик для отправки письма."""

    template = await fetch_template_by_id(message_data["template_id"])

    if template.template_name == 'welcome_letter':  # {{ username }}
        context = {"username": message_data["user"]["username"]}
    elif template.template_name == 'summary_letter':  # {{ movie_list }
        content_summary = await fetch_content_summary(message_data["user"]["user_id"])
        movie_list = [movie.title for movie in content_summary.movies]
        context = {"movie_list": ", ".join(movie_list)}
    elif template.template_name == 'test_letter':  # {{ current_datetime }}
        context = {"current_datetime": datetime.now()}
    elif template.template_name == 'likes_summary_letter':  # {{ username }} {{ likes_count }}
        since = datetime.now() - timedelta(days=1)  # временно отдаём информацию о лайках за прошедший день.
        ugc_data = await fetch_ugc_summary(message_data["user"]["user_id"], since=since)
        context = {"username": message_data["user"]["username"], "new_likes": ugc_data.new_likes}
    else:
        raise Exception(f"Unknown template name: {template.template_name}")
    rendered_content = Template(template.template_content).render(context)
    message_data["email_body"] = rendered_content
    return await process_email_simple(message_data)


async def process_email_simple(message_data):
    """Просто отправляет готовое письмо,

    если вдруг не указан subject, парсим и подставляем title"""
    if 'subject' not in message_data:
        subject = extract_title(message_data["email_body"])
    else:
        subject = message_data["subject"]

    user_notification = {
        "contact": message_data["email"],
        "subject": subject,
        "content": message_data["email_body"]
    }
    mail = MailNotification(user_notification)
    mail.prepare_message()
    await mail.send()
    logger.info(f"Письмо отправлено: {user_notification['contact']}")


async def one_processor_to_rule_them_all(message: aio_pika.IncomingMessage, rabbitmq_: RabbitMQ):
    """Единый обработчик для почтовых сообщений.

    Существует договорённость, если передаётся template_id - требуется темплэйтинг письма на стороне воркера.
    В случае ошибок,- сообщение перенаправляется в worker_dead_letters на последующую обработку.
    Архитектурно позволяет держать одну общую очередь.
    После успешной отправки письма, сообщение транслируется в очередь выполняющую функцию лога.
    """
    async with message.process():
        message_data = json.loads(message.body)

        try:
            if "template_id" in message_data and message_data["template_id"]:
                await processor_with_templating(message_data)
            else:
                await process_email_simple(message_data)
            await produce_log_letter(message, rabbitmq_)
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {type(e)}:{e}")
            await produce_dead_letter_queue_message(message_data, rabbitmq_)


@logger.catch
async def produce_dead_letter_queue_message(message_data: dict, rabbitmq_: RabbitMQ):
    """ Ожидает ~5 минут до отправки сообщения в DLQ """
    await asyncio.sleep(settings.dead_letter_sleep_delay)
    if 'dlq_retry' in message_data:
        if message_data['dlq_retry'] >= settings.dead_letter_max_retries:
            logger.error(f"Достигнуто максимальное количество повторений обработки в DLQ. msg: {message_data}")
            return
        message_data['dlq_retry'] += 1
    else:
        message_data['dlq_retry'] = 1
    try:
        await rabbitmq_.publish("worker_dead_letters", message_data)
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения в DLQ: {type(e)}:{e}")
    logger.warning(f"Сообщение перемещено в dead_letter_queue.")


def extract_title(html_content):
    """Извлекает title из html-кода"""
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.text if title_tag else None


@logger.catch
async def produce_log_letter(message: aio_pika.IncomingMessage, rabbitmq_: RabbitMQ):
    await rabbitmq_.publish_incoming_message(config_rabbit.log_queue, message)
