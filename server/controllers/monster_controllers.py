import json

from app import db
from models.encounter_models import *
from models.monster_models import *


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
    create_spell_list(monster_stats, m)

    db.session.commit()
    return m


def dump_monster(m: Monster) -> dict:
    return {
        "name": m.name,
        "size": m.size,
        "type": m.type,
        "alignment": m.alignment,
        "ac": m.ac,
        "hp": m.hp,
        "hit_dice": m.hit_dice,
        "speed": m.speed,
        "stats": {
            "strength": m.strength,
            "dexterity": m.dexterity,
            "constitution": m.constitution,
            "intelligence": m.intelligence,
            "wisdom": m.wisdom,
            "charisma": m.charisma
        },
        "saves": {
            "strength": m.strength_save,
            "dexterity": m.dexterity_save,
            "constitution": m.constitution_save,
            "intelligence": m.intelligence_save,
            "wisdom": m.wisdom_save,
            "charisma": m.charisma_save
        },
        "skills": {
            "acrobatics": m.acrobatics,
            "animal_handling": m.animal_handling,
            "arcana": m.arcana,
            "athletics": m.athletics,
            "deception": m.deception,
            "history": m.history,
            "insight": m.insight,
            "intimidation": m.intimidation,
            "investigation": m.investigation,
            "medicine": m.medicine,
            "nature": m.nature,
            "perception": m.perception,
            "persuasion": m.persuasion,
            "religion": m.religion,
            "sleight_of_hand": m.sleight_of_hand,
            "stealth": m.stealth,
            "survival": m.survival
        },
        "vulnerabilities": m.vulnerabilities,
        "resistances": m.resistances,
        "damage_immunities": m.damage_immunities,
        "condition_immunities": m.condition_immunities,
        "senses": m.senses,
        "languages": m.languages,
        "cr": m.cr,
        "traits": [{"name": t.name, "desc": t.description} for t in m.traits] if m.traits else [],
        "actions": [{"name": a.name, "desc": a.description} for a in m.actions] if m.actions else [],
        "legendary_actions": [{"name": la.name, "desc": la.description} for la in m.legendary_actions] if m.legendary_actions else [],
        "reactions": [{"name": r.name, "desc": r.description} for r in m.reactions] if m.legendary_actions else [],
        "spell_list": {
            "desc": m.spell_list["desc"] if m.spell_list is not None and m.spell_list["desc"] is not None else None,
            "cantrips": m.spell_list["cantrips"].split(",") if m.spell_list is not None and m.spell_list["cantrips"] is not None else [],
            "first": m.spell_list["first"].split(",") if m.spell_list is not None and m.spell_list["first"] is not None else [],
            "second": m.spell_list["second"].split(",") if m.spell_list is not None and m.spell_list["second"] is not None else [],
            "third": m.spell_list["third"].split(",") if m.spell_list is not None and m.spell_list["third"] is not None else [],
            "fourth": m.spell_list["fourth"].split(",") if m.spell_list is not None and m.spell_list["fourth"] is not None else [],
            "fifth": m.spell_list["fifth"].split(",") if m.spell_list is not None and m.spell_list["fifth"] is not None else [],
            "sixth": m.spell_list["sixth"].split(",") if m.spell_list is not None and m.spell_list["sixth"] is not None else [],
            "seventh": m.spell_list["seventh"].split(",") if m.spell_list is not None and m.spell_list["seventh"] is not None else [],
            "eighth": m.spell_list["eighth"].split(",") if m.spell_list is not None and m.spell_list["eighth"] is not None else [],
            "ninth": m.spell_list["ninth"].split(",") if m.spell_list is not None and m.spell_list["ninth"] is not None else []
        },
        "source": m.source
    }


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
    spells = monster_stats["spell_list"]

    # If a monster doesn't have cantrips or first level spells, they probably dont have any higher level ones
    if spells["cantrips"] == [] or spells["first"] == []:
        return None

    s = SpellList(monster_id=monster.id)

    s.cantrips = ",".join(spells["cantrips"]) if ",".join(spells["cantrips"]) != "" else None
    s.first = ",".join(spells["first"]) if ",".join(spells["first"]) != "" else None
    s.second = ",".join(spells["second"]) if ",".join(spells["second"]) != "" else None
    s.third = ",".join(spells["third"]) if ",".join(spells["third"]) != "" else None
    s.fourth = ",".join(spells["fourth"]) if ",".join(spells["fourth"]) != "" else None
    s.fifth = ",".join(spells["fifth"]) if ",".join(spells["fifth"]) != "" else None
    s.sixth = ",".join(spells["sixth"]) if ",".join(spells["sixth"]) != "" else None
    s.seventh = ",".join(spells["seventh"]) if ",".join(spells["seventh"]) != "" else None
    s.eighth = ",".join(spells["eighth"]) if ",".join(spells["eighth"]) != "" else None
    s.ninth = ",".join(spells["ninth"]) if ",".join(spells["ninth"]) != "" else None

    db.session.add(s)

    return s