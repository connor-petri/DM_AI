from flask import request
from flask_login import login_required, current_user
from app import app

from controllers.encounter_controllers import create_new_encounter, get_encounter_json


@app.route("/generate_encounter", methods=["POST"])
@login_required
def generate_encounter():
    return create_new_encounter(request.args.get("prompt", default="", type=str), user_id=current_user.id)


@app.route("/encounter", methods=["GET"])
@login_required
def get_encounter():
    return get_encounter_json(request.args.get("id", type=int), user_id=current_user.id)
