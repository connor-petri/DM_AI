from groq import Groq

def generate_encounter(client: Groq, system_content: str, user_content: str, temp: float=0.2, stream: bool=True) -> list:
    return client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": "!E_JSON " + user_content,
                "type": "json_object"
            }
        ],
        temperature=temp,
        max_tokens=1024,
        top_p=1,
        stream=stream,
        stop=None,
    )
