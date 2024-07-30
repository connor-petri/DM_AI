from dotenv import load_dotenv
import os
from groq import Groq

from encounter import generate_encounter

if __name__ == '__main__':
    load_dotenv()
    API_KEY = os.getenv("GROQ_API_KEY")

    if API_KEY is None:
        raise ValueError("API_KEY is not set in .env file")

    client = Groq(api_key=API_KEY)

    with open("sysprompt.txt", "r") as f:
        system_content = f.read()

    encounter = generate_encounter(client, system_content, input("Prompt: "))
    encounter.printEncounter()