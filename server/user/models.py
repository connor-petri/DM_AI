from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)

    _password = db.Column('password', db.String(255), nullable=False)

    encounters = db.relationshop('Encounter', backref='user', lazy=True)

    def _get_password(self):
        return self._password
    
    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password', 
                          descriptor=property(_get_password, 
                                              _set_password))
    

