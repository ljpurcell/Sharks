from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .user import User
from app import db


class LoginForm(FlaskForm):
    username: StringField = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Username"})
    password: PasswordField = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Password"})
    submit: SubmitField = SubmitField('Log in!')


class UserDetailsForm(FlaskForm):
    username: StringField = StringField(validators=[InputRequired(), Length(min=4,max=30)])
    password: PasswordField = PasswordField(validators=[InputRequired(), Length(min=4,max=30)])
    email: EmailField = EmailField(validators=[InputRequired()])
    mobile: StringField = StringField(validators=[InputRequired()])
    submit: SubmitField = SubmitField('Save!')

    def validate_username(self, username: str):
        existing_username: str = db.one_or_404(db.select(User).filter_by(username=username.data))

        if existing_username:
            flash("That username is already taken, sorry.")
            raise ValidationError("That username is already taken, sorry.")
        


class RegistrationForm(FlaskForm):
    username: StringField = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Username"})
    password: PasswordField = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Password"})
    email: EmailField = EmailField(validators=[InputRequired()], render_kw={"placeholder":"Email"})
    mobile: StringField = StringField(validators=[InputRequired()],render_kw={"placeholder":"Mobile"})
    submit: SubmitField = SubmitField('Register!')
        


