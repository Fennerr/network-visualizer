# rich_logger.py

from rich.logging import RichHandler
import logging


def get_rich_logger():
    """
    Configures and returns a logger with RichHandler.
    """
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logger = logging.getLogger("rich")
    return logger
