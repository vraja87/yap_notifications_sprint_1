import logging
import json

from typing import Type

from fastapi.encoders import jsonable_encoder
from aio_pika import Message, connect_robust, Connection, Channel


class QueueProducer:
    def __init__(self, dsn):
        self.dsn: str = dsn
        self.connection: Connection = None
        self.channel: Channel = None

    async def connect_broker(self) -> None:
        self.connection = await connect_robust(self.dsn)
        self.channel = await self.connection.channel()
        logging.info("Connected to %s", self.dsn)

    async def close(self):
        try:
            await self.connection.close()
        except Exception as e:
            logging.error("Error closing connection")
            raise e

    async def publish(self, message: dict, routing_key) -> str:
        encoded_message = jsonable_encoder(message)
        await self.channel.default_exchange.publish(
            Message(body=json.dumps(encoded_message).encode('utf-8')),
            routing_key=routing_key)
        return 'ok'


queue_producer: QueueProducer = None


async def get_producer() -> Type[QueueProducer]:
    return queue_producer
