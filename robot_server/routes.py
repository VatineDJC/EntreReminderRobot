from flask import Flask
from ._event_dispatch import feishu_event_handler

def register(app: Flask):
    # for example
    app.add_url_rule("/feishu_events", methods=["POST"], view_func=feishu_event_handler)
