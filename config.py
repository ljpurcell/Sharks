from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

from os import path, environ as env
basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = env.get('SECRET_KEY') or 'secret'
    SECURITY_SALT = env.get('SECURITY_SALT') or 'salt'
    MAIL_SERVER = env.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(env.get('MAIL_PORT', 587))
    MAIL_USE_TLS = env.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = env.get('GMAIL_USERNAME') 
    MAIL_PASSWORD = env.get('GMAIL_APP_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = env.get('SECRET_KEY')
    REDIS_URL = env.get('REDIS_URL') or 'redis://'
    TWILIO_ACCOUNT_SID=env.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN=env.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER=env.get('TWILIO_PHONE_NUMBER')
    MY_NUMBER=env.get('MY_NUMBER')
    

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    APP_URL='localhost'
    ENV="development"
    DEBUG = True
    SERVER_NAME='127.0.0.1:5000' 
    SQLALCHEMY_DATABASE_URI = env.get('DEV_DATABASE_URL', 'sqlite:///' + path.join(basedir, 'data-dev.sqlite'))
    PREFERRED_URL_SCHEME='http'
    

class TestingConfig(Config):
    ENV="testing"
    TESTING = True
    APP_URL='http://127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI = env.get('TEST_DATABASE_URL', 'sqlite://')
    PREFERRED_URL_SCHEME='http'



class ProductionConfig(Config):
    ENV="production"
    TESTING = False
    DEBUG = False
    SERVER_NAME='' # TODO
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', 'sqlite:///' + path.join(basedir, 'data.sqlite'))
    PREFERRED_URL_SCHEME='https'



config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}