import logging

from .logging import slog


logger = logging.getLogger(__name__)


def payment() -> str:
    logger.info("start handling payment")
    logger.info("charge customer", extra=slog(amount=10, customer="johndoe"))
    logger.info("payment succeeds")
    return "payment"
