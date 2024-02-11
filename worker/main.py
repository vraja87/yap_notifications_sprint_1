import asyncio

from aiohttp import web
from src.config import config_rabbit
from src.connector.rabbit import RabbitMQ
from src.processor import one_processor_to_rule_them_all


async def main(rabbitmq_: RabbitMQ):
    # Словарь соответствия очередей и их обработчиков
    queues_handlers = {
        "smtp.v1.immediate_messages": (
            lambda message: one_processor_to_rule_them_all(message, rabbitmq_=rabbitmq_),
            10,
        ),
        "smtp.v1.common_messages": (
            lambda message: one_processor_to_rule_them_all(message, rabbitmq_=rabbitmq_),
            5,
        ),
        "smtp.v1.worker_dead_letters": (
            lambda message: one_processor_to_rule_them_all(message, rabbitmq_=rabbitmq_),
            3,
        ),
    }

    for queue_name, (handler, priority) in queues_handlers.items():
        # Объявление очередей с разными приоритетами
        await rabbitmq.declare_queue(queue_name, priority)
        # Настройка обработчиков сообщений для каждой очереди
        await rabbitmq.consume(queue_name, handler)
    # Превентивно создаём очередь для логирования успешных сообщений.
    await rabbitmq.declare_queue(config_rabbit.log_queue, priority=3, ttl=config_rabbit.log_ttl)

    await asyncio.Future()


async def healthcheck(request):  # noqa
    return web.Response(text="OK")


async def start_healthcheck_server():
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    rabbitmq = RabbitMQ(config_rabbit.uri)
    loop.run_until_complete(rabbitmq.connect())
    try:
        loop.run_until_complete(start_healthcheck_server())
        loop.run_until_complete(main(rabbitmq))
    finally:
        loop.run_until_complete(rabbitmq.close())
        loop.close()
