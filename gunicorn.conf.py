import multiprocessing
import os

from dotenv import load_dotenv
import yaml
import sentry_sdk

from app.logging import Slog

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    default_integrations=False,
    traces_sample_rate=0.0,
    before_send=Slog.sentry_before_send,
)

with open("logging.yaml") as f:
    logconfig_dict = yaml.load(f, Loader=yaml.Loader)
    logconfig_dict["handlers"]["otp_slack"]["url"] = os.getenv("OTP_SLACK_WEBHOOK_URL", "")

bind = "0.0.0.0:3000"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "app:app"
