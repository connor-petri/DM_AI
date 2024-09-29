from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)

    password = db.Column(db.String(255), nullable=False)
    

