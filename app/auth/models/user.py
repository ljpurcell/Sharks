from app import db
from flask_login import UserMixin, current_user
from flask_bcrypt import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app


user_votes = db.Table('user_votes', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),  
    db.Column('vote_assignment_id', db.Integer, db.ForeignKey('vote_assignments.id'))                                                        
)

class VoteAssignment(db.Model):
    __tablename__ = 'vote_assignments'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.String(5), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    vote_giver = db.Column(db.Integer, nullable=False)
    vote_getter = db.Column(db.Integer, nullable=False)
    num_votes = db.Column(db.Integer, nullable=False)


class GameRSVP(db.Model):
    __tablename__ = 'game_rsvps'
    id = db.Column(db.Integer, primary_key=True)
    game_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_playing = db.Column(db.Boolean, nullable=False)


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
    game_rsvps = db.relationship('GameRSVP', backref='user')
    votes = db.relationship('VoteAssignment',
                            secondary=user_votes,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    

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
    
    @staticmethod
    def update_details(database, data):
        hashed_password = generate_password_hash(data.password.data)
        user_to_update = User.query.filter_by(id=current_user.id).first()
        user_to_update.username=data.username.data
        user_to_update.password_hash=hashed_password
        user_to_update.email=data.email.data
        user_to_update.mobile=data.mobile.data
        database.session.commit()
        return user_to_update 

    
    def generate_email_token(self, email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-email/' + serializer.dumps(email, salt="email-token")

    def confirm_email_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
            return email
        except Exception:
            return False
        
    def generate_mobile_token(self, mobile):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return app.config['APP_URL'] + '/confirm-mobile/' + serializer.dumps(mobile, salt="mobile-token")
        
    def confirm_mobile_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            mobile = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
            return mobile
        except Exception:
            return False

    def generate_rsvp_token(self, date):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        details = [self.id, date]
        return app.config['APP_URL'] + '/rsvp/' + serializer.dumps(details, salt="rsvp-token")
        
    def confirm_rsvp_token(self, token, expiration=86400):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            response = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
            return response
        except Exception:
            return False
        

