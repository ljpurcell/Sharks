from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


mail: Mail = Mail()
db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_type: str="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)


    with app.app_context():
        from .auth import auth as auth_blueprint
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        db.create_all()


    return app



app = create_app("production")