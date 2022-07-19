from plugins.controller.event_handler import event_handler
from flask import Flask


def register(app: Flask):
    # for example
    app.add_url_rule("/", methods=["POST"], view_func=event_handler)
