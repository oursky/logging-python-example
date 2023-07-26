import json
import urllib.request
from datetime import datetime
from logging import NOTSET, Formatter, Handler

LOG_RECORD_KEY = "slog"
"""
LOG_RECORD_KEY is the attribute name of where to store a Slog in a LogRecord.
"""

MESSAGE_KEY = "message"
"""
MESSAGE_KEY is the key to store the original message of a LogRecord in a Slog.
"""


class SlogFormatter(Formatter):
    def formatMessage(self, record):
        """
        If the record has a Slog, rewrite the message.
        """
        if hasattr(record, LOG_RECORD_KEY):
            slog_ = getattr(record, LOG_RECORD_KEY)
            slog_[MESSAGE_KEY] = record.message
            record.message = str(slog_)
        return super().formatMessage(record)

    def formatTime(self, record, datefmt=None):
        """
        Format as RFC3339.
        """
        dt = datetime.utcfromtimestamp(record.created)
        return dt.isoformat(timespec="milliseconds") + "Z"


class Slog:
    def __init__(self, dict_):
        self.dict_ = dict_

    def __str__(self):
        """
        Override __str__ to format a Slog.
        """
        return " ".join(f"{k}={self[k]}" for k in self)

    def __iter__(self):
        """
        Override __iter__ to alter the iteraction order so that message comes first.
        """
        if MESSAGE_KEY in self.dict_:
            yield MESSAGE_KEY
        for k in self.dict_:
            if k != MESSAGE_KEY:
                yield k

    def __getitem__(self, k):
        """
        Override __getitem__ to make Slog works like a dict.
        """
        return self.dict_[k]

    def __setitem__(self, k, v):
        """
        Override __setitem__ to make Slog works like a dict.
        """
        self.dict_[k] = v

    @classmethod
    def sentry_before_send(cls, event, hint):
        """
        sentry_before_send is the integration between Slog and Sentry.
        It adds Slog to the contexts of a Sentry event.

        See https://docs.sentry.io/platforms/python/guides/logging/configuration/filtering/#using-platformidentifier-namebefore-send-
        """
        if "log_record" in hint:
            log_record = hint["log_record"]
            if hasattr(log_record, LOG_RECORD_KEY):
                slog_ = getattr(log_record, LOG_RECORD_KEY)
                if "contexts" in event:
                    # Values in contexts must be builtin Python objects.
                    # So we cannot simply pass slog_ here.
                    event["contexts"][LOG_RECORD_KEY] = slog_.dict_
        return event


def slog(**kwargs):
    """
    slog is a shortcut to create a Slog.

    logger.info("my message %s", "hello", extra=slog(a=b, c=d))
    """
    return {LOG_RECORD_KEY: Slog(dict_=kwargs)}


class SlackHandler(Handler):
    def __init__(self, level=NOTSET, url=""):
        super().__init__(level)
        self.url = url

    def emit(self, record):
        try:
            data = json.dumps({"text": record.message}).encode()
            r = urllib.request.Request(
                self.url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(r):
                pass
        except Exception:
            self.handleError(record)
