from json import json
from flask import jsonify
from flask_login import user_loader, login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

from app import db
from ..models.user import User


@user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


def authenticate_user(data: json):
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({"status:": "error", 
                        "message": "Missing username or password."}), 400

    user = User.query.filter_by(username=username)

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"status": "success",
                        "message": "Logged in."}), 200
    else:
        return jsonify({"status": "error",
                        "message": "Invalid username or password."}), 401
    

def register_user(data: json):
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({"status:": "error", 
                        "message": "Missing username or password."}), 400
    
    if User.query.filter_by(username=username):
        return jsonify({"status:": "error", 
                        "message": "Username is already in use."}), 400
    
    try:
        hashed_password = generate_password_hash(data.get('password'))
        db.session.add(User(username=username, password=hashed_password))
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error",
                        "message": str(e)}), 500


    
    
    return "Registeration Failed"