from flask import Flask

from .root import root
from .payment import payment
from .otp import otp


app = Flask("app")
app.add_url_rule("/", None, root)
app.add_url_rule("/payment", None, payment)
app.add_url_rule("/otp", None, otp)
