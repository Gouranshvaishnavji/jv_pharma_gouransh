import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)

def setup_logger(level=logging.INFO):
 

    if len(logging.getLogger().handlers) > 0:
        return logging.getLogger()

    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    for noisy_logger in ["uvicorn.access", "uvicorn.error", "fastapi"]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    logger.info("informant  initialized successfully")
    return logger


