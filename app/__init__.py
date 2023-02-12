from flask import Flask, flash, request, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
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
        

    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(30), unique=True)
        password_hash = db.Column(db.String(80), nullable=False)
        mobile = db.Column(db.String, nullable=False)
        email = db.Column(db.String)

        def __repr__(self):
            return '<User %r>' % self.name

    class RegistrationForm(FlaskForm):
        # Look into validation options for each
        username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Username"})
        password = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Password"})
        email = EmailField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Email"})
        mobile = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Mobile"})
        submit = SubmitField('Register!')

        def validate_username(self, username):
            existing_username = User.query.filter_by(
                username=username.data
            ).first()

            if existing_username:
                raise ValidationError("That username is already taken, sorry.")


    class LoginForm(FlaskForm):
        # Look into validation options for each
        username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Username"})
        password = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Password"})
        submit = SubmitField('Log in!')


    with app.app_context():
        db.create_all()


    return app