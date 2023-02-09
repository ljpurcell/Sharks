from os import path, environ as env
basedir = path.abspath(path.dirname(__file__))

class Config:
    MAIL_SERVER = env.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(env.get('MAIL_PORT', 587))
    MAIL_USE_TLS = env.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = env.get('GMAIL_USERNAME') 
    MAIL_PASSWORD = env.get('GMAIL_APP_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.get('DEV_DATABASE_URL', 'sqlite:///' + path.join(basedir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = env.get('TEST_DATABASE_URL', 'sqlite://')



class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', 'sqlite:///' + path.join(basedir, 'data.sqlite'))



config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}