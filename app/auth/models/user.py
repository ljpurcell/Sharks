from app import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    is_confirmed_email = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_on = db.Column(db.DateTime)
    mobile = db.Column(db.String, nullable=False)
    is_confirmed_mobile = db.Column(db.Boolean, nullable=False, default=False)
    mobile_confirmed_on = db.Column(db.DateTime)
    

    def __repr__(self):
        return '<User %r>' % self.username
    
    @staticmethod
    def create_new_user(database, data):
        hashed_password = generate_password_hash(data.password.data)
        new_user = User(
            username=data.username.data, 
            password_hash=hashed_password, 
            email=data.email.data,
            is_confirmed_email=False,
            email_confirmed_on=None,
            mobile=data.mobile.data,
            is_confirmed_mobile=False,
            mobile_confirmed_on=None,
            )
        database.session.add(new_user)
        database.session.commit()
        return new_user 
    
    def generate_email_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-email/' + serializer.dumps(email, salt=app.config['SECURITY_SALT'])
    
    def generate_mobile_token(mobile):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-mobile/' + serializer.dumps(mobile, salt=app.config['SECURITY_SALT'])

    def confirm_email_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
            return email
        except Exception:
            return False
        
    def confirm_mobile_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            mobile = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
            return mobile
        except Exception:
            return False