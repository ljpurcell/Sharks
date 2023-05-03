from flask import redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import check_password_hash
from flask_mail import Message
from app import db, login_manager, mail, create_app
from ..auth.models.form import LoginForm, UserDetailsForm, RegistrationForm
from ..auth.models.user import User
from . import auth
from os import environ as env
import datetime
from rq import Queue
from worker import conn

q = Queue(connection=conn)


@login_manager.user_loader
def load_user(user_id: int | str) -> User:
    return db.get_or_404(User, int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalars(db.select(User).filter_by(username=form.username.data)).first()
        if user:
            if check_password_hash(user.pw_hash, form.password.data):
                login_user(user, remember=True)
                flash('You are logged in!', category='success')
                return redirect(url_for('main.index', user=current_user))
        flash('Incorrect details. Please try again.', category='error')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user: User = User.create_new_user(database=db, data=form)
        login_user(user, remember=True)
        flash('Nice! You will be sent a verification email and text shortly.',
              category='success')
        q.enqueue(send_async_welcome_email, user.id)
        q.enqueue(send_async_welcome_text, user.id)
        return redirect(url_for('main.index', user=user))

    return render_template('auth/register.html', form=form)


@auth.route('/my-profile', methods=['POST', 'GET'])
@login_required
def my_profile():
    form = UserDetailsForm()
    if form.validate_on_submit():
        user = User.update_details(database=db, data=form)
        login_user(user, remember=True)
        flash('Nice! You succesfully updated your details.', category='success')

    return render_template('auth/user.html', user=current_user, form=form)


@auth.route('/confirm-email/<token>')
@login_required
def confirm_email(token: str):
    if current_user.is_confirmed_email:
        flash('Email already confirmed', 'success')
        return redirect(url_for('main.index'))

    email: str = current_user.confirm_email_token(token)
    user: User = db.select(User).filter_by(email=current_user.email)

    if user.email == email:
        user.is_confirmed_email = True
        user.email_confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Email confirmed!', 'success')
    else:
        flash('Confirmation link invalid or expired', 'error')

    return redirect(url_for('main.index'))


@auth.route('/confirm-mobile/<token>')
@login_required
def confirm_mobile(token: str):
    if current_user.is_confirmed_mobile:
        flash('Mobile already confirmed', 'success')
        return redirect(url_for('main.index'))

    mobile = current_user.confirm_mobile_token(token)
    user = db.one_or_404(db.select(User).filter_by(mobile=current_user.mobile))

    if user.mobile == mobile:
        user.is_confirmed_mobile = True
        user.mobile_confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Mobile confirmed!', 'success')
    else:
        flash('Confirmation link invalid or expired', 'error')

    return redirect(url_for('main.index'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Log out successful', category='success')
    return redirect(url_for('auth.login'))


def send_async_welcome_email(user_id: int | str) -> None:
    app = create_app("production")

    with app.app_context():
        user: User = db.get_or_404(User, int(user_id))
        msg: Message = Message(
            '[SharksApp] - Welcome', sender=env.get("GMAIL_USERNAME"), recipients=[user.email])
        msg.subject = 'Welcome!'
        msg.body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link: ' + \
            user.generate_email_token(user.email)
        mail.send(msg)


def send_async_welcome_text(user_id: int | str):
    from twilio.rest import Client
    app = create_app("production")
    with app.app_context():
        user: User = db.get_or_404(User, int(user_id))
        client: Client = Client(
            app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
        message_body = f'Hi {user.username}!\n\nPlease verify your mobile by clicking this link and following the prompts: ' + \
            user.generate_mobile_token(user.mobile)
        message = client.messages.create(
            body=message_body,
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=user.mobile
        )
