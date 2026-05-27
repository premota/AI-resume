import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_loggers(level: int = logging.INFO):
    root_logger = logging.getLogger()

    formatter = logging.Formatter(fmt=LOG_FORMAT, style="%", datefmt=DATE_FORMAT)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)
    root_logger.setLevel(level)
