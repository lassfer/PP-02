
import logging
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "mastertool.log"

def get_logger(name="mastertool"):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
