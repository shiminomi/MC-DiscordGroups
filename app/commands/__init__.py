import logging

from discord import Message, Guild, Client, Member


logger = logging.getLogger(__name__)

supported_commands = {}

def command_class(cls):
    supported_commands[cls.__name__.lower()] = cls


# Take messages if they are commands. Every message here is guaranteed
# to be a command.
async def handle_command(message: Message, client: Client, prefix):
    # Intercept Bot DMs
    if not message.guild:
        return

    content = message.content[len(prefix):]
    cmd = content.split()[0].lower()

    if cmd in supported_commands:
        command = supported_commands[cmd](message, client, content)
        await command.handle()
        return


# Command class template
class Command:

    def __init__(self, message: Message = None, client: Client = None, content: str = None):
        if not message:
            raise ValueError("You must issue a command with a message or guild")
        self.message: Message = message
        self.guild: Guild = message.guild
        self.client = client
        self.args = content.split()[1:]


    async def handle(self):
        raise AttributeError("Must be overwritten by command class")



## DO NOT MOVE THIS CODE
# The following imports all the modules in command so that they can be added to the
# command interpreter.
import pkgutil

__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module