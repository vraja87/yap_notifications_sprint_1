import logging
import json

from typing import Type

from fastapi.encoders import jsonable_encoder
from aio_pika import Message, connect_robust


class QueueProducer:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None

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


class QueueProducerImmediate:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None

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
        await self.connect_broker()
        encoded_message = jsonable_encoder(message)
        await self.channel.default_exchange.publish(
            Message(body=json.dumps(encoded_message).encode('utf-8')),
            routing_key=routing_key)
        await self.close()
        return 'ok'


queue_producer = QueueProducer
queue_producer_immediate = QueueProducer


async def get_producer() -> Type[QueueProducer]:
    return queue_producer


async def get_producer_immediate() -> Type[QueueProducerImmediate]:
    return queue_producer_immediate
