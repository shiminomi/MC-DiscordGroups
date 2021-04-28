import logging
import json

from os import path

logger = logging.getLogger(__name__)

f_loc = "guild_data.json"

empty_data = {
    "factions": {},
    "invites": {}
}
# Invite will have a faction faction_name key into a list of user ids

empty_faction = {
    "name": "",
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


def add_faction(faction_name, creator, role_id, category_id, text_channel_id, voice_channel_id):
    data = get_json()

    if faction_name not in data["factions"]:
        faction = dict(empty_faction)
        faction["name"] = faction_name
        faction["leader"] = creator
        faction["role"] = role_id
        faction["category_id"] = category_id
        faction["text_channel"] = text_channel_id
        faction["voice_channel"] = voice_channel_id
        faction["members"].append(creator)
        data["factions"][faction_name] = faction
        data["invites"][faction_name] = []

    save_json(data)


def remove_faction(faction_name):
    data = get_json()

    if faction_name in data["factions"]:
        del data["factions"][faction_name]
    if faction_name in data["invites"]:
        del data["invites"][faction_name]

    save_json(data)


def add_invite(faction_name, user_id):
    data = get_json()

    if faction_name in data["factions"] and faction_name in data["invites"]:
        data["invites"][faction_name].append(user_id)
    
    save_json(data)


def remove_invite(faction_name, user_id):
    data = get_json()

    if faction_name in data["factions"] and faction_name in data["invites"]:
        if user_id in data["invites"][faction_name]:
            data["invites"][faction_name].remove(user_id)
    
    save_json(data)


def get_faction(faction_name):
    data = get_json()

    if faction_name in data["factions"]:
        return data["factions"][faction_name]

    return None


def faction_exists(faction_name):
    data = get_json()
    return faction_name in data["factions"]


def get_user_faction(user_id):
    data = get_json()

    for faction in data["factions"]:
        if user_id in data["factions"][faction]["members"]:
            return data["factions"][faction]
    
    return None