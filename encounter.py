from groq import Groq
import json

class Encounter:
    def __init__(self, monster_json: json, intro_text: str):
        self.monster_json = monster_json
        self.intro_text = intro_text

    def printEncounter(self) -> None:
        print(self.intro_text)
        print(self.monster_json)


def generate_encounter(client: Groq, system_content: str, user_content: str, temp: float=0.2) -> list:
    monster_json = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": "!E_JSON " + user_content
            }
            
        ],
        temperature=temp,
        stream=False,
        response_format={"type": "json_object"}
    ).choices[0].message.content

    intro = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": "!E_INTRO " + user_content,
            }
        ],
        temperature=temp,
        stream=False
    ).choices[0].message.content

    return Encounter(monster_json, intro)
