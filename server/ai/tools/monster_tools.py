from app import db
from models.monster_models import *


def get_unique_monster_types() -> list:
    return db.session.query(Monster.type).distinct().all()


def get_monster_names_by_type(monster_type: str) -> list[str]:
    return db.session.query(Monster.name).filter_by(type=monster_type).all()


# Returns data useful for encounter generation and deciding which tools to use.
def get_relevent_monster_data(name: str) -> dict:
    m: Monster = Monster.query.filter_by(name=name).first()
    return {
        "name": m.name,
        "cr": m.cr,
        "has_traits": bool(m.traits),
        "has_actions": bool(m.actions),
        "has_legendary_actions": bool(m.legendary_actions),
        "has_spell_list": bool(m.spell_list)
    }


def get_traits(name: str) -> list[dict]:
    return [{"name": trait.name, 
             "desc": trait.desc} 
             for trait in Trait.query.filter_by(monster_id=Monster.query.filter_by(name=name).first()).all()]


def get_actions(name: str) -> list[dict]:
    return [{"name": action.name, 
             "desc": action.desc}
             for action in Action.query.filter_by(monster_id=Monster.query.filter_by(name=name).first()).all()]


def get_legendary_actions(name: str) -> list[dict]:
    return [{"name": la.name,
             "desc": la.desc}
             for la in LegendaryAction.query.filter_by(monster_id=Monster.query.filter_by(name=name).first()).all()]


def get_spell_list(name: str) -> dict:
    s: SpellList = SpellList.query.filter_by(monster_id=Monster.query.filter_by(name=name).first()).first()
    if not s: return {}

    s_dict = {}
    if s.desc:
        s_dict["desc"] = s.desc
    if s.cantrips:
        s_dict["cantrips"] = s.cantrips
    if s.first:
        s_dict["first_level"] = s.first
    if s.second:
        s_dict["second_level"] = s.second
    if s.third:
        s_dict["third_level"] = s.third
    if s.fourth:
        s_dict["fourth_level"] = s.fourth
    if s.fifth:
        s_dict["fifth_level"] = s.fifth
    if s.sixth:
        s_dict["sixth_level"] = s.sixth
    if s.seventh:
        s_dict["seventh_level"] = s.seventh
    if s.eighth:
        s_dict["eighth_level"] = s.eighth
    if s.ninth:
        s_dict["ninth_level"] = s.ninth

    return s_dict
    

# Update when new tools are added.
monster_tools = {
    "get_uniqu_monster_types": get_unique_monster_types,
    "get_monster_names_by_type": get_monster_names_by_type,
    "get_relevent_monster_data": get_relevent_monster_data,
    "get_traits": get_traits,
    "get_actions": get_actions,
    "get_legendary_actions": get_legendary_actions,
    "get_spell_list": get_spell_list
}