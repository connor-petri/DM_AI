import json
from app import db
from models.monster_models import *


def load_lib_1():
    with open("scripts/data/monsterlib1.json", 'r') as f:
        data = json.load(f)

    for monster in data["monsters"]:
        match = Monster.query.filter_by(name=monster[0]).first()
        if match:
            print(f"{monster[0]} found. Skipping...")
            continue

        print(f"Loading {monster[0]}...")


        m = Monster()
        stats = monster[1]

        m.name = stats["name"]
        m.size = stats["size"]
        m.type = stats["type"]
        try:
            m.alignment = stats["alignment"]
        except KeyError:
            m.alignment = ""
        m.ac = stats["ac"]
        m.hp = stats["hp"]
        m.hit_dice = stats["hit_dice"]
        try:
            m.speed = stats["speed"]
        except KeyError:
            m.speed = "30 ft."

        m.strength = stats["stats"][0]
        m.dexterity = stats["stats"][1]
        m.constitution = stats["stats"][2]
        m.intelligence = stats["stats"][3]
        m.wisdom = stats["stats"][4]
        m.charisma = stats["stats"][5]

        m.strength_save = 0
        m.dexterity_save = 0
        m.constitution_save = 0
        m.intelligence_save = 0
        m.wisdom_save = 0
        m.charisma_save = 0

        for save in stats["saves"]:
            key, value = next(iter(save.items()))
            if key == "undefined":
                break
            setattr(m, key.lower().replace(" ", "_") + "_save", value)

        m.acrobatics = 0
        m.animal_handling = 0
        m.arcana = 0
        m.athletics = 0
        m.deception = 0
        m.history = 0
        m.insight = 0
        m.intimidation = 0
        m.investigation = 0
        m.medicine = 0
        m.nature = 0
        m.perception = 0
        m.persuasion = 0
        m.religion = 0
        m.sleight_of_hand = 0
        m.stealth = 0
        m.survival = 0

        for save in stats["skillsaves"]:
            key, value = next(iter(save.items()))
            if key == "":
                break
            setattr(m, key.lower().replace(" ", "_"), value)

        try:
            m.vulnerabilities = stats["damage_vulnerabilities"]
        except KeyError:
            m.vulnerabilities = ""

        try:
            m.resistances = stats["damage_resistances"]
        except KeyError:
            m.resistances = ""

        try:
            m.damage_immunities = stats["damage_immunities"]
        except KeyError:
            m.damage_immunities = ""

        try:
            m.condition_immunities = stats["condition_immunities"]
        except KeyError:
            m.condition_immunities = ""

        try:
            m.senses = stats["senses"]
        except KeyError:
            m.senses = ""

        try:
            m.languages = stats["languages"]
        except KeyError:
            m.languages = ""
        
        try:
            m.cr = stats["cr"] if int(stats["cr"]) != 0 else "-"
        except ValueError:
            m.cr = stats["cr"] if stats["cr"] != "" else "-"
        except KeyError:
            m.cr = "-"

        for trait in stats["traits"]:
            m.source = trait["desc"] if trait["name"] == "Source" else stats["source"]

        db.session.add(m)
        db.session.commit()

        for trait in stats["traits"]:
            if trait["name"] == "Source":
                continue

            t = Trait(name=trait["name"], desc=trait["desc"], monster_id=m.id)
            db.session.add(t)
            db.session.commit()

        for action in stats["actions"]:
            a = Action(name=action["name"], desc=action["desc"], monster_id=m.id)
            db.session.add(a)
            db.session.commit()

        for la in stats["legendary_actions"]:
            la = LegendaryAction(name=la["name"], desc=la["desc"], monster_id=m.id)
            db.session.add(la)
            db.session.commit()

        for reaction in stats["reactions"]:
            r = Reaction(name=reaction["name"], desc=reaction["desc"], monster_id=m.id)
            db.session.add(r)
            db.session.commit()

        if stats["spells"] != []:
            s = SpellList(monster_id=m.id)
            try:
                spells = stats["spells"]
                s.desc = spells[0]
                s.cantrips = spells[1]
                s.first = spells[2]
                s.second = spells[3]
                s.third = spells[4]
                s.fourth = spells[5]
                s.fifth = spells[6]
                s.sixth = spells[7]
                s.seventh = spells[8]
                s.eighth = spells[9]
                s.ninth = spells[10]
            except IndexError:
                pass
            finally:
                db.session.add(s)
                db.session.commit()

        print(f"Successfully loaded {monster[0]}!")