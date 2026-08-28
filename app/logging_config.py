import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger("customer_churn_api")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=1_000_000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger