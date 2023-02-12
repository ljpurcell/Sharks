from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .user import User

class RegistrationForm(FlaskForm):
    # Look into validation options for each
    username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder":"Password"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder":"Email"})
    mobile = StringField(validators=[InputRequired()],render_kw={"placeholder":"Mobile"})
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