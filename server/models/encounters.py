from app import db


monster_encounter = db.Table('monster_encounter',
                             db.Column('encounter_id', db.Integer, db.ForeignKey('encounters.id'), primary_key=True),
                             db.Column('monster_id', db.Integer, db.ForeignKey('monsters.id'), primary_key=True),
                             db.Column('monster_count', db.Integer, nullable=False, default=1))


class Encounter(db.Model):
    __tablename__ = 'encounters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    monsters = db.relationship('Monster', backref=__tablename__, secondary=monster_encounter, lazy=True)


class Monster(db.Model):
    __tablename__ = 'monsters'
    
    id = db.Column(db.Integer, primary_key=True)

    encounters = db.relationship('Encounter', backref=__tablename__, secondary=monster_encounter, lazy=True)

    # info
    name = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    alignment = db.Column(db.String(20), nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    hit_dice = db.Column(db.String(30), nullable=False)
    speed = db.Column(db.String(50), nullable=False)

    # stats
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)

    # saves
    strength_save = db.Column(db.Integer, nullable=False)
    dexterity_save = db.Column(db.Integer, nullable=False)
    constitution_save = db.Column(db.Integer, nullable=False)
    intelligence_save = db.Column(db.Integer, nullable=False)
    wisdom_save = db.Column(db.Integer, nullable=False)
    charisma_save = db.Column(db.Integer, nullable=False)

    # skills
    acrobatics = db.Column(db.Integer, nullable=False)
    animal_handling = db.Column(db.Integer, nullable=False)
    arcana = db.Column(db.Integer, nullable=False)
    athletics = db.Column(db.Integer, nullable=False)
    deception = db.Column(db.Integer, nullable=False)
    history = db.Column(db.Integer, nullable=False)
    insight = db.Column(db.Integer, nullable=False)
    intimidation = db.Column(db.Integer, nullable=False)
    investigation = db.Column(db.Integer, nullable=False)
    medicine = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.Integer, nullable=False)
    perception = db.Column(db.Integer, nullable=False)
    persuasion = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.Integer, nullable=False)
    sleight_of_hand = db.Column(db.Integer, nullable=False)
    stealth = db.Column(db.Integer, nullable=False)
    survival = db.Column(db.Integer, nullable=False)

    vulnerabilities = db.Column(db.String(100))
    resistances = db.Column(db.String(100))
    damage_immunities = db.Column(db.String(100))
    condition_immunities = db.Column(db.String(100))
    senses = db.Column(db.String(50))
    languages = db.Column(db.String(50))
    cr = db.Column(db.Integer, nullable=False)

    traits = db.relationship('Trait', backref='monster', lazy=True)
    spells = db.relationship('Spell', backref='monster', lazy=True)
    actions = db.relationship('Action', backref='monster', lazy=True)
    legendary_actions = db.relationship('LegendaryAction', backref='monster', lazy=True)
    reactions = db.relationship('Reaction', backref='monster', lazy=True)

    source = db.Column(db.String(50))


class Trait(db.Model):
    __tablename__ = 'traits'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


class Spell(db.Model):
    __tablename__ = 'spells'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


class LegendaryAction(db.Model):
    __tablename__ = 'legendary_actions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))  


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))  