from flask import jsonify
from flask_login import current_user
import json
from jsonschema import validate
from sqlalchemy.exc import SQLAlchemyError
import os

from app import db
from resources.settings import client
from models.encounters import *
from controllers.monsters import *


def groq_encounter_json(system_content: str, user_content:str, json_schema: json) -> json:
    return json.loads(client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_content + " using the json schema: " + json.dumps(json_schema),
                }
            ],
            temperature=0.15,
            stream=False,
            response_format={"type": "json_object"}
        ).choices[0].message.content)


def check_encounter_json(data: json) -> bool:
    with open(os.getcwd() + "/resources/json_schemas/new_encounter_schema.json") as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False

    


def create_new_encounter(user_content: str):
    try:
        # Load the system content from a file
        with open(os.getcwd() + "/resources/sysprompts/json_requests.txt", "r") as f:
            system_content: str = f.read()

        # Load the JSON schema for the encounter
        with open(os.getcwd() + "/resources/json_schemas/new_encounter_schema.json", "r") as f:
            schema: json = json.load(f)

        # Request a chat completion from the model, passing in the system and user content, and the JSON schema
        encounter_json = groq_encounter_json(system_content, user_content, schema)

        while not check_encounter_json(encounter_json):
            print("Invalid schema. Retrying")
            encounter_json = groq_encounter_json(system_content, user_content, schema)

        # print(encounter_json)

        #Database Operations
        encounter = Encounter(user_id=current_user.id)
        db.session.add(encounter)
        db.session.commit()

        monsters: list[Monster] = get_encounter_monster_list(encounter_json)

        print("here")
        
        for i in range(len(encounter_json["monsters"])):
            db.session.execute(
                monster_encounter.insert().values(
                    encounter_id=encounter.id,
                    monster_id=monsters[i].id,
                    monster_count=encounter_json["monsters"][i]["count"]
                )
            )

        db.session.commit()

        return jsonify({"status": "success",
                        "message": f"Encounter created successfully with encounter_id {encounter.id}",
                        "encounter_id": encounter.id}), 200

    
    except Exception as e:
        print(e)
        return jsonify({"status": "error",
                        "message": str(e)}), 500