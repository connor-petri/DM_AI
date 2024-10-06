import json
from flask import request, jsonify
from flask_login import login_required
from app import app
from resources.settings import client

from controllers.encounters import create_new_encounter, get_encounter_json


@app.route("/generate_encounter", methods=["POST"])
@login_required
def generate_encounter():
    return create_new_encounter(request.args.get("prompt", default="", type=str))


@app.route("/encounter", methods=["GET"])
@login_required
def get_encounter():
    return get_encounter_json(request.args.get("id", type=int))


@app.route("/encounter-intro", methods=["GET"])
def generate_intro():
    try:

        with open("./resources/sysprompts/story_requests.txt", "r") as f:
            system_content: str = f.read()

        user_prompt: str = request.args.get("prompt", default="", type=str)
        encounter_summary: str = request.args.get("encounter_summary", default="", type=str)

        return jsonify(client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": "Write an intro to an encounter using the prompt: " + user_prompt + " and using the following summary " + encounter_summary
                }
            ],
            temperature=0.3,
            stream=False
        ).choices[0].message.content)
    
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)})
    




