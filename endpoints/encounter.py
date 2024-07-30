import json
from flask import request, jsonify
from endpoints.app import app
from resources.settings import client


@app.route("/encounter-json", methods=["GET"])
def generate_encounter():
    try:

        # Load the system content from a file
        with open("./resources/sysprompt.txt", "r") as f:
            system_content: str = f.read()

        # Get the user content from the query string
        user_content: str = request.args.get("prompt", default="", type=str)

        # Load the JSON schema for the encounter
        with open("./resources/schema.json", "r") as file:
            schema: json = json.load(file)

        # Request a chat completion from the model, passing in the system and user content, and the JSON schema
        return jsonify(client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_content + " using the json schema: " + json.dumps(schema),
                }
            ],
            temperature=0.15,
            stream=False,
            response_format={"type": "json_object"}
        ).choices[0].message.content)
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


@app.route("/encounter-intro", methods=["GET"])
def generate_intro():
    with open("./resources/sysprompt.txt", "r") as f:
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