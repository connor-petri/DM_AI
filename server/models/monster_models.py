from app import db
from models.encounter_models import *


class Monster(db.Model):
    __tablename__ = 'monsters'
    
    id = db.Column(db.Integer, primary_key=True)

    encounters = db.relationship('EncounterMonsterAssociation', back_populates='monster', lazy=True)

    # info
    name = db.Column(db.String(250), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    alignment = db.Column(db.String(100))
    ac = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    hit_dice = db.Column(db.String(100))
    speed = db.Column(db.String(250))

    # stats
    strength = db.Column(db.Integer, nullable=False, default=10)
    dexterity = db.Column(db.Integer, nullable=False, default=10)
    constitution = db.Column(db.Integer, nullable=False, default=10)
    intelligence = db.Column(db.Integer, nullable=False, default=10)
    wisdom = db.Column(db.Integer, nullable=False, default=10)
    charisma = db.Column(db.Integer, nullable=False, default=10)

    # saves
    strength_save = db.Column(db.Integer, nullable=False, default=0)
    dexterity_save = db.Column(db.Integer, nullable=False, default=0)
    constitution_save = db.Column(db.Integer, nullable=False, default=0)
    intelligence_save = db.Column(db.Integer, nullable=False, default=0)
    wisdom_save = db.Column(db.Integer, nullable=False, default=0)
    charisma_save = db.Column(db.Integer, nullable=False, default=0)

    # skills
    acrobatics = db.Column(db.Integer, nullable=False, default=0)
    animal_handling = db.Column(db.Integer, nullable=False, default=0)
    arcana = db.Column(db.Integer, nullable=False, default=0)
    athletics = db.Column(db.Integer, nullable=False, default=0)
    deception = db.Column(db.Integer, nullable=False, default=0)
    history = db.Column(db.Integer, nullable=False, default=0)
    insight = db.Column(db.Integer, nullable=False, default=0)
    intimidation = db.Column(db.Integer, nullable=False, default=0)
    investigation = db.Column(db.Integer, nullable=False, default=0)
    medicine = db.Column(db.Integer, nullable=False, default=0)
    nature = db.Column(db.Integer, nullable=False, default=0)
    perception = db.Column(db.Integer, nullable=False, default=0)
    persuasion = db.Column(db.Integer, nullable=False, default=0)
    religion = db.Column(db.Integer, nullable=False, default=0)
    sleight_of_hand = db.Column(db.Integer, nullable=False, default=0)
    stealth = db.Column(db.Integer, nullable=False, default=0)
    survival = db.Column(db.Integer, nullable=False, default=0)

    vulnerabilities = db.Column(db.String(250))
    resistances = db.Column(db.String(250))
    damage_immunities = db.Column(db.String(250))
    condition_immunities = db.Column(db.String(250))
    senses = db.Column(db.String(250))
    languages = db.Column(db.String(250))
    cr = db.Column(db.String(10), nullable=False)

    traits = db.relationship('Trait', backref=__tablename__, lazy=True)
    actions = db.relationship('Action', backref=__tablename__, lazy=True)
    legendary_actions = db.relationship('LegendaryAction', backref=__tablename__, lazy=True)
    reactions = db.relationship('Reaction', backref=__tablename__, lazy=True)
    spell_list = db.relationship("SpellList", backref=__tablename__, lazy=True, uselist=False)

    source = db.Column(db.String(250))

# FIXME: Make a model for generated monsters
# class GeneratedMonster(Monster):
#     __tablename__ = 'generated_monsters'


class EncounterMonsterAssociation(db.Model):
    __tablename__ = 'encounter_monster_association'

    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'), primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), primary_key=True)
    count = db.Column(db.Integer, db.CheckConstraint('count>=0'), nullable=False)
    encounter = db.relationship('Encounter', back_populates='monsters')
    monster = db.relationship('Monster', back_populates='encounters')


class Trait(db.Model):
    __tablename__ = 'traits'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(3500))


class SpellList(db.Model):
    __tablename__ = 'spell_lists'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)

    desc = db.Column(db.String(500))

    cantrips = db.Column(db.String(500))
    first = db.Column(db.String(500))
    second = db.Column(db.String(500))
    third = db.Column(db.String(500))
    fourth = db.Column(db.String(500))
    fifth = db.Column(db.String(500))
    sixth = db.Column(db.String(500))
    seventh = db.Column(db.String(500))
    eighth = db.Column(db.String(500))
    ninth = db.Column(db.String(500))


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(3500))


class LegendaryAction(db.Model):
    __tablename__ = 'legendary_actions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(3500))  


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(3500))  