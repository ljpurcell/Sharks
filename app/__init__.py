from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from dotenv import load_dotenv
from config import config


# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = '/Users/LJPurcell/Code/Sharks/.env'
load_dotenv(dotenv_path=dotenv_path)

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
celery = Celery(__name__, broker= 'redis://localhost:6379/0')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_type="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app', 'app.tasks'])


    import json
    print(__name__, '\n' + json.dumps(celery.conf, indent=2, default=str), '\n')

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    return app



