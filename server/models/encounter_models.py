from app import db

from models.user_models import *


class Encounter(db.Model):
    __tablename__ = 'encounters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    monsters = db.relationship('EncounterMonsterAssociation', back_populates='encounter', lazy=True)


User.encounters = db.relationship('Encounter', backref=User.__tablename__, lazy=True)


