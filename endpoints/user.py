from hashlib import sha256
from os import getenv, urandom
from flask_login import UserMixin
from flask import request
import flask_login

from .app import app, db, login_manager


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.passhash = password

    def __repr__(self):
        return f"User({self.username})"
    
    def get_id(self) -> int:
        return self.user_id
    

@login_manager.user_loader
def loader_user(user_id: int) -> Users:
    return Users.query.get(user_id)


@app.route("/register", methods=["POST"])
def register():
    user = Users(request.form.get("username"), request.form.get("password"))
    db.session.add(user)
    db.session.commit()

    if Users.query.filter_by(username=user.username).first():
        return "User created successfully"
    else:
        return "Error creating user"
    

@app.route("/login", methods=["POST"])
def login():
    user: Users = Users.query.filter_by(username=request.form.get("username")).first()

    if user is not None and user.passhash == request.form.get("password"):
        flask_login.login_user(user)
        return "Logged in successfully"
    else:
        return "Invalid username or password"
    

@app.route("/logout", methods=["GET"])
def logout():
    if not flask_login.current_user.is_authenticated:
        return "Error logging out. You may already be logged out."
    
    flask_login.logout_user()
    return "Logged out successfully"
