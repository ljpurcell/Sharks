from flask import Flask, flash, request, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import path, environ as env
from dotenv import load_dotenv
from config import config

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = '/Users/LJPurcell/Code/Sharks/.env'
load_dotenv(dotenv_path=dotenv_path)

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_type="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
        

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        password_hash = db.Column(db.String, nullable=False)
        mobile = db.Column(db.String, nullable=False)
        email = db.Column(db.String)

        def __repr__(self):
            return '<User %r>' % self.name

    with app.app_context():
        db.create_all()


    return app