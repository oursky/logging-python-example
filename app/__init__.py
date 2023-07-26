from flask import Flask

from .otp import otp
from .payment import payment
from .root import root

app = Flask("app")
app.add_url_rule("/", None, root)
app.add_url_rule("/payment", None, payment)
app.add_url_rule("/otp", None, otp)
