import logging
import json

from os import path

logger = logging.getLogger(__name__)

f_loc = "guild_data.json"

empty_data = {
    "factions": {}
}

empty_factions = {
    "leader": 0,
    "role": 0,
    "category_id": 0,
    "text_channel": 0,
    "voice_channel": 0,
    "members": []
}


def create_json():
    if not path.exists(f_loc):
        with open(f_loc, "w") as f:
            f.write(json.dumps(empty_data))


def get_json():
    create_json()
    with open(f_loc, "r") as f:
        data = json.loads(f.read())
    
    return data


def save_json(data):
    create_json()
    with open(f_loc, "w") as f:
        f.write(json.dumps(data))


def add_faction(name, creator, role_id, category_id, text_channel_id, voice_channel_id):
    data = get_json()

    if name not in data["factions"]:
        faction = dict(empty_factions)
        faction["leader"] = creator
        faction["role"] = role_id
        faction["category_id"] = category_id
        faction["text_channel"] = text_channel_id
        faction["voice_channel"] = voice_channel_id
        faction["members"].append(creator)
        data["factions"][name] = faction

    save_json(data)


def remove_faction(name):
    data = get_json()

    if name in data["factions"]:
        del data["factions"][name]

    save_json(data)


def get_faction(name):
    data = get_json()

    if name in data["factions"]:
        return data["factions"][name]

    return None


def faction_exists(name):
    data = get_json()
    return name in data["factions"]