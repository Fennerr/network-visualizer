# rich_logger.py

from rich.logging import RichHandler
import logging


def get_rich_logger():
    """
    Configures and returns a logger with RichHandler.
    """
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    # logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    # logging.getLogger("s3transfer").setLevel(logging.CRITICAL)

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                tracebacks_theme="solarized-dark",
            )
        ],
    )

    logger = logging.getLogger("rich")
    return logger
