import logging
from .config import get_config
from .app import App


def setup_logger(app: App, logger: logging.Logger) -> None:
    config = get_config(app)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(config.logging_level)
