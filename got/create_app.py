from flask import Flask
from config import Config


def create_got_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from got.api import api
    api.init_app(app,
                 version='1.0',
                 title='Python Challenge Microservices',
                 description='GOT')

    return app
