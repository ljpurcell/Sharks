from flask import redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from . import auth
from .. import db, login_manager
from ..main.models.form import RegistrationForm, LoginForm
from ..main.models.user import User


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
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data, 
            password_hash=hashed_password, 
            mobile=form.mobile.data,
            email=form.email.data
            )
        db.session.add(new_user).commit()
        login_user(new_user, remember=True)
        flash('You are logged in!', category='success')
        # Send async email notifying of registration
        return redirect(url_for('main.index', user=current_user))

    return render_template('auth/register.html', form=form)
    

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Log out successful', category='success')
    return redirect(url_for('auth.login'))