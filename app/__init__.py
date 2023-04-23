from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis
from rq import Queue
from dotenv import load_dotenv
from config import config


# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = '/Users/LJPurcell/Code/Sharks/.env'
load_dotenv(dotenv_path=dotenv_path)

mail: Mail = Mail()
db: SQLAlchemy = SQLAlchemy()
queue: Queue = Queue(connection=Redis())
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_type: str="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue('shark-tasks', connection=app.redis)

    with app.app_context():
        from .auth import auth as auth_blueprint
        from .main import main as main_blueprint
        from .main.api import api as api_blueprint
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(api_blueprint)
        db.create_all()


    return app



app = create_app()