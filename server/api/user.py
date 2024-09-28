from flask import request, jsonify
from flask_login import user_loader, login_user, login_required, logout_user


from app import app, db, login_manager
from ..models.user import User
from ..controllers.user import authenticate_user, register_user





@app.route('/login', methods=['POST'])
def login():
    return authenticate_user(request.get_json())
    
    
    

@app.route('/register', methods=['POST'])
def register():
    return register_user(request.get_json())


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
