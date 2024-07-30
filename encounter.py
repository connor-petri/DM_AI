from groq import Groq
import json

class Encounter:
    def __init__(self, monster_json: json, intro_text: str):
        self.monster_json = monster_json
        self.intro_text = intro_text

    def printEncounter(self) -> None:
        print(self.intro_text)
        print(json.dumps(self.monster_json))


def generate_encounter(client: Groq, system_content: str, user_content: str) -> list:
    with open("schema.json", "r") as file:
        schema: json = json.load(file)

    monster_json: json = json.loads(client.chat.completions.create(
        model="llama-3.1-70b-versatile",
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

    encounter_summary: str = ""

    for monster in monster_json["Monsters"]:
        encounter_summary += str(monster["count"]) + monster["name"]
        if monster["count"] > 1:
            encounter_summary += "s\n"
        else:
            encounter_summary += "\n"

    intro = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": "Write an intro to an encounter using the prompt: " + user_content + " and using the monsters: " + encounter_summary
            }
        ],
        temperature=0.3,
        stream=False
    ).choices[0].message.content

    return Encounter(monster_json, intro)
