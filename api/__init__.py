import logging.config
from pathlib import Path

logging.config.fileConfig(Path(__file__).parent / "logging.conf", disable_existing_loggers=False)
