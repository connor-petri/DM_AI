from app import app, db
from models.user_models import *
from models.encounter_models import *
from models.monster_models import *


if __name__ == "__main__":
    with app.app_context():
        db.create_all()