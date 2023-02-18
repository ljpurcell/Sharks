from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String)
    mobile = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username