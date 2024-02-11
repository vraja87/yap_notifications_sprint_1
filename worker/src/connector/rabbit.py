import json
from abc import ABC
from typing import Callable

from aio_pika import IncomingMessage, Message, connect_robust
from aio_pika.abc import (AbstractRobustChannel, AbstractRobustConnection,
                          AbstractRobustQueue)
from src.logger import logger


class AbstractQueueInternal(ABC):
    async def connect(self) -> None:
        pass

    async def publish(self, queue_name: str, message: dict) -> str:
        pass

    async def consume(self, queue_name: str, callback_function: Callable):
        pass

    async def close(self):
        pass


class RabbitMQ(AbstractQueueInternal):
    """Обрабатывает параллельно несколько очередей, создает их при необходимости, с разными приоритетами."""

    connection: AbstractRobustConnection
    channel: AbstractRobustChannel
    queue_name: str
    queues: dict[str, AbstractRobustQueue]

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.queues = {}

    async def connect(self):
        self.connection = await connect_robust(self.dsn)
        self.channel = await self.connection.channel()

    async def declare_queue(self, queue_name: str, priority: int = 5, ttl: int = None):
        """Создаём очередь, задавая приоритет и при необходимости ttl."""
        arguments = {"x-max-priority": priority}
        if ttl:
            arguments["x-message-ttl"] = ttl
        queue = await self.channel.declare_queue(queue_name, durable=True, arguments=arguments)
        self.queues[queue.name] = queue
        logger.info(f"Queue '{queue_name}' with priority {priority} is ready")

    async def publish(self, queue_name: str, message: dict):
        if queue_name not in self.queues:
            logger.error(f"Queue '{queue_name}' not declared")
            return
        encoded_message = json.dumps(message).encode('utf-8')
        await self.channel.default_exchange.publish(
            Message(body=encoded_message),
            routing_key=queue_name
        )

    async def publish_incoming_message(self, queue_name: str, incoming_message: IncomingMessage):
        """ Для переотправки сообщения без изменений."""
        await self.channel.default_exchange.publish(
            Message(body=incoming_message.body),
            routing_key=queue_name
        )

    async def consume(self, queue_name: str, callback_function):
        if queue_name not in self.queues:
            logger.error(f"Queue '{queue_name}' not declared")
            return
        await self.queues[queue_name].consume(callback_function)
        logger.info(f"Worker started. Waiting for messages in '{queue_name}'")

    async def close(self):
        await self.channel.close()
        await self.connection.close()
        logger.info("Close connection, channel.")
