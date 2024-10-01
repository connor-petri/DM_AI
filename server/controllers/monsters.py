import json

from app import db
from models.encounters import *


def get_encounter_monster_list(encounter_data: json) -> list[Monster]:
    monster_list = []

    for monster in encounter_data["monsters"]:
        existing_monster = check_existing_monster(monster['statblock'])

        if existing_monster:
            monster_list.append(existing_monster)
        else:
            monster_list.append(create_new_monster_entry(monster["statblock"]))

    return monster_list


# Name and CR determine a match
def check_existing_monster(monster_stats: json) -> Monster:
    monsters: list[Monster] = Monster.query.filter_by(name=monster_stats["name"]).all()
    
    for monster in monsters:
        if monster.cr == monster_stats['cr']:
            return monster
    
    return None


def create_new_monster_entry(monster_stats: json) -> Monster:
    m = Monster()

    m.name = monster_stats["name"]
    m.size = monster_stats["size"]
    m.type = monster_stats["type"]
    m.alignment = monster_stats["alignment"]
    m.ac = monster_stats["ac"]
    m.hp = monster_stats["hp"]
    m.hit_dice = monster_stats["hit_dice"]
    m.speed = monster_stats["speed"]

    m.strength = monster_stats["stats"]["strength"]
    m.dexterity = monster_stats["stats"]["dexterity"]
    m.constitution = monster_stats["stats"]["constitution"]
    m.intelligence = monster_stats["stats"]["intelligence"]
    m.wisdom = monster_stats["stats"]["wisdom"]
    m.charisma = monster_stats["stats"]["charisma"]

    m.strength_save = monster_stats["saves"]["strength"]
    m.dexterity_save = monster_stats["saves"]["dexterity"]
    m.constitution_save = monster_stats["saves"]["constitution"]
    m.intelligence_save = monster_stats["saves"]["intelligence"]
    m.wisdom_save = monster_stats["saves"]["wisdom"]
    m.charisma_save = monster_stats["saves"]["charisma"]

    m.acrobatics = monster_stats["skills"]["acrobatics"]
    m.animal_handling = monster_stats["skills"]["animal_handling"]
    m.arcana = monster_stats["skills"]["arcana"]
    m.athletics = monster_stats["skills"]["athletics"]
    m.deception = monster_stats["skills"]["deception"]
    m.history = monster_stats["skills"]["history"]
    m.insight = monster_stats["skills"]["insight"]
    m.intimidation = monster_stats["skills"]["intimidation"]
    m.investigation = monster_stats["skills"]["investigation"]
    m.medicine = monster_stats["skills"]["medicine"]
    m.nature = monster_stats["skills"]["nature"]
    m.perception = monster_stats["skills"]["perception"]
    m.performance = monster_stats["skills"]["performance"]
    m.persuasion = monster_stats["skills"]["persuasion"]
    m.religion = monster_stats["skills"]["religion"]
    m.sleight_of_hand = monster_stats["skills"]["sleight_of_hand"]
    m.stealth = monster_stats["skills"]["stealth"]
    m.survival = monster_stats["skills"]["survival"]

    m.vulnerabilities = monster_stats["vulnerabilities"]
    m.resistances = monster_stats["resistances"]
    m.damage_immunities = monster_stats["damage_immunities"]
    m.condition_immunities = monster_stats["condition_immunities"]
    m.senses = monster_stats["senses"]
    m.languages = monster_stats["languages"]
    m.cr = monster_stats["cr"]
    m.source = monster_stats["source"]

    db.session.add(m)
    db.session.commit()

    create_traits(monster_stats, m)
    create_actions(monster_stats, m)
    create_reactions(monster_stats, m)
    create_legendary_actions(monster_stats, m)

    db.session.commit()
    return m


def create_traits(monster_stats: json, monster: Monster) -> list[Trait]:
    if monster_stats["traits"] == []:
        return []

    traits = [
        Trait(name=trait["name"], 
              description=trait["desc"], 
              monster_id=monster.id
        ) 
        for trait in monster_stats["traits"]
    ]

    for trait in traits:
        db.session.add(trait)

    return traits


def create_actions(monster_stats: json, monster: Monster) -> list[Action]:
    if monster_stats["actions"] == []:
        return []
    
    actions = [
        Action(name=action["name"], 
              description=action["desc"], 
              monster_id=monster.id
        ) 
        for action in monster_stats["actions"]
    ]

    for action in actions:
        db.session.add(action)

    return actions


def create_legendary_actions(monster_stats: json, monster: Monster) -> list[LegendaryAction]:
    if monster_stats["legendary_actions"] == []:
        return []

    l_actions = [
        LegendaryAction(name=la["name"], 
              description=la["desc"], 
              monster_id=monster.id
        ) 
        for la in monster_stats["legendary_actions"]
    ]

    for la in l_actions:
        db.session.add(la)

    return l_actions


def create_reactions(monster_stats: json, monster: Monster) -> list[Reaction]:
    if monster_stats["reactions"] == []:
        return []
    
    reactions = [
        Trait(name=r["name"], 
              description=r["desc"], 
              monster_id=monster.id
        ) 
        for r in monster_stats["reactions"]
    ]

    for r in reactions:
        db.session.add(r)

    return reactions


def create_spell_list(monster_stats: json, monster: Monster) -> SpellList:
    s = SpellList(monster_id=monster.id)
    spells = monster_stats["spell_list"]

    s.cantrips = ",".join(spells["cantrips"])
    s.first = ",".join(spells["first"])
    s.second = ",".join(spells["second"])
    s.third = ",".join(spells("third"))
    s.fourth = ",".join(spells["fourth"])
    s.fifth = ",".join(spells["fifth"])
    s.sixth = ",".join(spells["sixth"])
    s.seventh = ",".join(spells["seventh"])
    s.eighth = ",".join(spells["eighth"])
    s.ninth = ",".join(spells["ninth"])

    db.session.add(s)

    return s