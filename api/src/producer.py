import logging
import json

from fastapi.encoders import jsonable_encoder
from aio_pika import Message, connect

from core.config import settings


class RabbitMQ:
    def __init__(self, dsn):
        logging.error(settings.PRODUCER_DSN)
        self.dsn = dsn
        self.connection = None
        self.queue = None

    # @backoff.on_exception(backoff.expo, AMQPConnectionError, max_time=60, raise_on_giveup=True)
    async def connect_broker(self) -> None:
        self.connection = await connect(self.dsn)
        logging.info("Connected to %s", self.dsn)

    async def close(self):
        try:
            await self.connection.close()
        except Exception as e:
            logging.error("Error closing connection")
            raise e

    async def create_queue(self, ):
        async with self.connection.channel() as channel:
            self.queue = await channel.declare_queue(settings.QUEUE_NAME, durable=True, arguments={"x-max-priority":10})
            logging.info("Queue '%s' created", self.queue.name)

    async def publish(self, message: dict) -> str:
        await self.connect_broker()
        encoded_message = jsonable_encoder(message)
        if not self.queue:
            await self.create_queue()
        async with self.connection.channel() as channel:
            await channel.default_exchange.publish(Message(body=json.dumps(encoded_message).encode('utf-8')), routing_key=self.queue.name)
        return 'ok'


producer = RabbitMQ(settings.PRODUCER_DSN)
