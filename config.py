class Config(object):
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PeopleConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/pcdbpeople'


class PlacesConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/pcdbplaces'
