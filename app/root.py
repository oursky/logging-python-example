import logging

logger = logging.getLogger(__name__)


def root() -> str:
    1 / 0
    return "root"
