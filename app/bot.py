import logging

from commands import handle_command
from config import load_config, BotConfig
from discord import Client, Guild, Message

logger = logging.getLogger('mc_discordgroups-bot')


class Bot(Client):

    def __init__(self, cfg, **options):
        super().__init__(**options)
        self.user_cfg = cfg    

    async def on_ready(self):
        logger.info("Bot active. Reporting for duty.")


    async def on_message(self, message: Message):
        logger.info("Message intercepted from {0.author}: {0.content}".format(message))

        # Check if command
        prefix = self.user_cfg.discord_prefix
        if message.content[:len(prefix)] == prefix:
            await handle_command(message, self, prefix)
        
        #else:
        #    await handle_message(self, message, cfg)


def set_up_logs():
    FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                                  mode='a')
    handler.setFormatter(logging.Formatter(FORMAT))
    handler.setLevel(logging.INFO)

    logging.getLogger().addHandler(handler)

    logger.info("=========NEW SESSION=========")


if __name__ == "__main__":
    set_up_logs()
    global cfg
    cfg = load_config()
    
    if cfg:
        discord_client = Bot(cfg)

        token = cfg.discord_token
        prefix = cfg.discord_prefix

        discord_client.run(token)

    else:
        logger.error("Config failed to load, bot will not run.")