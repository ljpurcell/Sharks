from app import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False)
    is_confirmed_email = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_on = db.Column(db.DateTime)
    mobile = db.Column(db.String, nullable=False)
    

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
            )
        database.session.add(new_user)
        database.session.commit()
        return new_user 