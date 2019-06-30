from flask import Flask
from flask_migrate import Migrate
from python_challenge.mocks import populate_mocks


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from python_challenge.model import db
    db.init_app(app)
    Migrate(app, db)

    from python_challenge.api import api
    api.init_app(app,
                 version='1.0',
                 title='Python Challenge Microservices',
                 description='Manage peoples and kingdoms of Game of Throne')

    @app.cli.command()
    def seed():
        with app.app_context():
            populate_mocks(db)

    return app
