from dotenv import load_dotenv
from os import getenv
from groq import Groq

#Groq stuff
load_dotenv()
API_KEY = getenv("GROQ_API_KEY")

if API_KEY is None:
    raise ValueError("API_KEY is not set in .env file")

client = Groq(api_key=API_KEY)