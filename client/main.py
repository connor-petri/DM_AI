import requests
import json

ip = "http://127.0.0.1:5000"

session = requests.Session()


def login(username, password):
    data = json.dumps({"username": username,
                       "password": password})

    return session.post(ip + "/login", json=data)


def register(username, password):
    data = json.dumps({"username": username,
                        "password": password})
     
    return session.put(ip + "/register", json=data)


def generate_encounter(prompt: str):
    data = json.dumps({"prompt": prompt})

    return session.post(ip + "/generate_encounter", json=data)


while True:
    command_list: list = input().split(" ")

    response = None

    if not command_list or not command_list[0]:
        continue

    command = command_list[0]

    if command == "exit":
        exit()

    if command == "help":
        print("""
        exit - exit
        """)
        continue

    if command == 'logout':
        response = session.post(ip + "/logout")

    elif command == "login":
        if len(command_list) < 3:
            print("login [username] [password]")
            continue
        
        response = login(command_list[1], command_list[2])

    elif command == "register":
        if len(command_list) < 3:
            print("register [username] [password]")
            continue
        
        response = register(command_list[1], command_list[2])

    elif command == "generate_encounter":
        if len(command_list) < 2:
            print("generate_encounter [prompt]")
            continue

        prompt = " ".join(command[1:])

        response = generate_encounter(prompt)

    else:
        print("Invalid command")

    # print(f"{response.json['status']}: {response.json['message']}")
    if response:
        print(response.text)