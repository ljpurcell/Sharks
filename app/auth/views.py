from flask import redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import check_password_hash
from flask_mail import Message
from app import db, login_manager, queue, mail, create_app
from ..auth.token import confirm_token
from ..auth.models.form import RegistrationForm, LoginForm
from ..auth.models.user import User
from . import auth
from os import environ as env
import datetime


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
        flash('Nice! You will be sent a verification email shortly.', category='success')
        queue.enqueue(send_async_welcome_email, user.id)
        return redirect(url_for('main.index', user=user))

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.is_confirmed_email:
        flash('Email already confirmed', 'success')
        return redirect(url_for('main.index'))

    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    
    if user.email == email:
        user.is_confirmed_email = True
        user.email_confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Email confirmed!', 'success')
    else:
        flash('Confirmation link invalid or expired', 'error')
        
    return redirect(url_for('main.index'))
    

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Log out successful', category='success')
    return redirect(url_for('auth.login'))



def send_async_welcome_email(user_id):    
    app = create_app() 

    with app.app_context():
        user = User.query.get(int(user_id))
        msg = Message('[SharksApp] - Welcome', sender=env.get("GMAIL_USERNAME"), recipients=[user.email])
        msg.subject = 'Welcome!'
        msg.body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link: {url_for(user.generate_token(user.email), _external=True)}'
        mail.send(msg)



