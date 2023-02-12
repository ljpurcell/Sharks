from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user
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
                flash('Nice!')
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect details')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        db.session.add(User(
            username=form.username.data, 
            password_hash=hashed_password, 
            mobile=form.mobile.data,
            email=form.email.data
            ))
        db.session.commit()
        # Send async email notifying of registration
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
    

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))