import os

packages = ['flask', 'groq', 'python-dotenv', 'flask-login', 'psycopg2', 'sqlalchemy', 'sqlalchemy-utils']

for package in packages:
    os.system(f'pip install {package}')