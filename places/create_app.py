from flask import Flask
from flask_migrate import Migrate
from config import PlacesConfig


def create_places_app():
    app = Flask(__name__)
    app.config.from_object(PlacesConfig)

    from places.model import db
    db.init_app(app)
    Migrate(app, db)

    from places.api import api
    api.init_app(app,
                 version='1.0',
                 title='Python Challenge Microservices',
                 description='Places')

    @app.cli.command()
    def seed():
        from places.mocks.populate_mocks import populate_mocks
        with app.app_context():
            populate_mocks(db)

    return app
