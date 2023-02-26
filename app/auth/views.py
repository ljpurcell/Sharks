from flask import redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from . import auth
from .. import db, login_manager
from ..auth.models.form import RegistrationForm, LoginForm
from ..auth.models.user import User
from app.notifications.new_user_email import send_welcome_email

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=True)
                flash('You are logged in!', category='success')
                return redirect(url_for('main.index', user=current_user))
            else:
                flash('Incorrect details. Please try again.', category='error')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create_new_user(database=db, data=form)
        login_user(user, remember=True)
        flash('You are logged in!', category='success')
        send_welcome_email.delay(user.id)
        return redirect(url_for('main.index', user=user))

    return render_template('auth/register.html', form=form)
    

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Log out successful', category='success')
    return redirect(url_for('auth.login'))