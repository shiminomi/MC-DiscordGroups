import logging
import json

from os import path

logger = logging.getLogger('mc_discordgroups-bot')

class BotConfig():

    def __init__(self):

        cfg = {}
        if path.exists('../config.json'):
            with open('../config.json', 'r') as f:
                cfg = json.load(f)
        else:
            logger.error("No config file. Exiting.")
            quit()

        self.discord_token = cfg['discord']['token']
        self.discord_prefix = cfg['discord']['prefix']
        self.mongo_address = cfg['mongo']['address']


def load_config():
    return BotConfig()