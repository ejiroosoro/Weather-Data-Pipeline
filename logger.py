"""
logger.py
---------
Reusable logger for the whole project.
Logs to both terminal AND logs/pipeline.log file.

Usage in any file:
    from logger import get_logger
    log = get_logger(__name__)
    log.info("Something happened")
    log.error("Something broke")
"""

import logging
from config import LOG_DIR, LOG_FILE, LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger that writes to terminal + log file.

    Args:
        name: Pass __name__ from the calling module.

    Returns:
        logging.Logger
    """
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(name)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.DEBUG))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Terminal handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
