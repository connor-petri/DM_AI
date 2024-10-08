from flask import request, jsonify
from flask_login import login_required, logout_user
import json

from app import app, db, login_manager
from models.user_models import User
from controllers.user_controllers import authenticate_user, register_user


@app.route('/login', methods=['POST'])
def login():
    return authenticate_user(json.loads(request.get_json()))
    

@app.route('/register', methods=['PUT'])
def register():
    return register_user(json.loads(request.get_json()))


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({"status": "success",
                        "message": "Logged out."})
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)}), 500
