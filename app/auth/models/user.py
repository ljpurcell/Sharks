from app import db
from flask_login import UserMixin, current_user
from flask_bcrypt import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from typing import Any




user_votes = db.Table('user_votes', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),  
    db.Column('vote_assignment_id', db.Integer, db.ForeignKey('vote_assignments.id'))                                                        
)

class VoteAssignment(db.Model):
    __tablename__: str = 'vote_assignments'
    id: int = db.Column(db.Integer, primary_key=True)
    season_id: str = db.Column(db.String(5), nullable=False)
    round: int = db.Column(db.Integer, nullable=False)
    vote_giver: int = db.Column(db.Integer, nullable=False)
    vote_getter: int = db.Column(db.Integer, nullable=False)
    num_votes: int = db.Column(db.Integer, nullable=False)


class GameRSVP(db.Model):
    __tablename__: str = 'game_rsvps'
    id: int = db.Column(db.Integer, primary_key=True)
    game_date: str = db.Column(db.String(15), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_playing: bool = db.Column(db.Boolean, nullable=False)


class User(db.Model, UserMixin):
    __tablename__: str = 'users'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(30), unique=True)
    password_hash: bytes = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String, nullable=False)
    is_confirmed_email: bool = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_on: datetime = db.Column(db.DateTime)
    mobile: str = db.Column(db.String, nullable=False)
    is_confirmed_mobile: bool = db.Column(db.Boolean, nullable=False, default=False)
    mobile_confirmed_on: datetime = db.Column(db.DateTime)
    game_rsvps = db.relationship('GameRSVP', backref='user')
    votes = db.relationship('VoteAssignment',
                            secondary=user_votes,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    

    def __repr__(self):
        return '<User %r>' % self.username
    
    @staticmethod
    def create_new_user(database: SQLAlchemy, data: Any):
        hashed_password: str = generate_password_hash(data.password.data).decode('utf-8')
        mobile_globalised: str = User.try_globalise_number(data.mobile.data)
        new_user: User = User(
            username=data.username.data, 
            password_hash=hashed_password, 
            email=data.email.data,
            is_confirmed_email=False,
            email_confirmed_on=None,
            mobile=mobile_globalised,
            is_confirmed_mobile=False,
            mobile_confirmed_on=None,
            )
        database.session.add(new_user)
        database.session.commit()
        return new_user 
    
    @staticmethod
    def update_details(database: SQLAlchemy, data):
        hashed_password: bytes = generate_password_hash(data.password.data)
        user_to_update: User = db.get_or_404(User, int(current_user.id))
        user_to_update.username=data.username.data
        user_to_update.password_hash=hashed_password
        user_to_update.email=data.email.data
        user_to_update.mobile=data.mobile.data
        database.session.commit()
        return user_to_update 
    
    @staticmethod
    def try_globalise_number(mob_number: str) -> str:
        if len(mob_number) == 10 and mob_number[0] == '0':
            return "+61" + mob_number[1:]
        else:
            return mob_number

    
    def generate_email_token(self, email: str) -> str:
        serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-email/' + serializer.dumps(email, salt="email-token")

    def confirm_email_token(self, token: str, expiration: int = 3600) -> str | Exception:
        serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email: str = serializer.loads(token, salt="email-token", max_age=expiration)
            return email
        except Exception as err:
            return err
        
    def generate_mobile_token(self, mobile) -> str:
        serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-mobile/' + serializer.dumps(mobile, salt="mobile-token")
        
    def confirm_mobile_token(self, token: str, expiration: int = 3600)-> str | Exception:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            mobile: str = serializer.loads(token, salt="mobile-token", max_age=expiration)
            return mobile
        except Exception as err:
            return err

    def generate_rsvp_token(self, date_str: str) -> str:
        serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        details: tuple[int|str, str] = (self.id, date_str)
        return app.config['APP_URL'] + '/rsvp/' + serializer.dumps(details, salt="rsvp-token")
        
    def confirm_rsvp_token(self, token: str, expiration: int = 86400) -> str | Exception:
        serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            response: str = serializer.loads(token, salt="rsvp-token", max_age=expiration)
            return response
        except Exception as err:
            return err
        

