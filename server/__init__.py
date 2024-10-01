from app import app, db
from models.user import *
from models.encounters import *


if __name__ == "__main__":
    with app.app_context():
        db.create_all()