import logging
from logging.handlers import RotatingFileHandler


def setup_logger():

    logger = logging.getLogger()

    # prevent duplicate handlers on reload
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # console handler (Render captures this)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # file handler (local development)
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()