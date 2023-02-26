from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery, Task
from dotenv import load_dotenv
from os import environ as env
from config import config
from .celery. celeryconfig import celery_config

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = '/Users/LJPurcell/Code/Sharks/.env'
load_dotenv(dotenv_path=dotenv_path)

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_type="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)
    
    def celery_init_app(app: Flask) -> Celery:
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: object) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(__name__, task_cls=FlaskTask)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app


    app.config.from_mapping(
        CELERY=celery_config,
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    

    import json
    print(json.dumps(app.extensions['celery'].conf, indent=2, default=str), '\n')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    

    return app



