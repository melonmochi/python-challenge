from flask import Flask
from flask_migrate import Migrate


def create_people_app():
    app = Flask(__name__)
    app.config.from_object('config.PeopleConfig')

    from people.model import db
    db.init_app(app)
    Migrate(app, db)

    from people.api import api
    api.init_app(app,
                 version='1.0',
                 title='Python Challenge Microservices',
                 description='People')

    @app.cli.command()
    def seed():
        from people.mocks.populate_mocks import populate_mocks
        with app.app_context():
            populate_mocks(db)

    return app
