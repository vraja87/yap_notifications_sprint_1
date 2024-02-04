import json
import sys

from loguru import logger

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOG_DEFAULT_HANDLERS = ["console"]

LOG_FORMAT_JSON = '{"level":"{level}", "message":"{message}", "request_id": 123}'


def serialize(record):
    subset = {"timestamp":record["time"].timestamp(), "message":record["message"]}
    return json.dumps(subset)


def formatter(record):
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


# logger.add("/var/log/notifications/rotated.json", level="DEBUG", format=formatter, rotation="10 MB", retention="10 days", compression="zip", serialize=True, )
logger.add(sys.__stdout__, level="DEBUG")
logger.add(sys.stdout, level="INFO")
