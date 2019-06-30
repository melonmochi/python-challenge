class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/python-challenge'
    SQLALCHEMY_BINDS = {
        'people': 'postgresql://postgres:postgres@127.0.0.1/pcdbpeople',
        'places': 'postgresql://postgres:postgres@127.0.0.1/pcdbplaces'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
