from sys import argv

from app import app, db

from api.user_endpoints import *
from api.encounter_endpoints import *

from scripts.load_lib_1 import load_lib_1


if __name__ == '__main__':
    if len(argv) == 1:
        app.run(debug=True)

    elif argv[1] == '-s':
        if len(argv) < 3 or argv[2] not in ["db_create", "load_lib_1"]:
            print(
                '''Available scripts:
                -s init_db: Initialize the database.
                -s load_lib_1: Load Monster Library 1 into the database.'''
                )
            exit()

        if argv[2] == "db_create":
            with app.app_context():
                db.create_all()
                print("Database initialized.")
        
        elif argv[2] == "load_lib_1":
            with app.app_context():
                load_lib_1()
                print("Monster Library 1 loaded.")  
            
    else:
        print(
            '''-s: Run a script.'''
            )
