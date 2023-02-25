import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

from os import path, environ as env
basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = env.get('SECRET_KEY')
    MAIL_SERVER = env.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(env.get('MAIL_PORT', 587))
    MAIL_USE_TLS = env.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = env.get('GMAIL_USERNAME') 
    MAIL_PASSWORD = env.get('GMAIL_APP_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = env.get('SECRET_KEY')
    

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.get('DEV_DATABASE_URL', 'sqlite:///' + path.join(basedir, 'data-dev.sqlite'))
    CELERY_BROKER_URL = env.get('CELERY_BROKER_URL')

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