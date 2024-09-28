from app import app, db
import user.models
import encounters.models


if __name__ == "__main__":
    with app.app_context():
        db.create_all()