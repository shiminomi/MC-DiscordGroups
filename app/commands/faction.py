# !faction <create|remove> (name)
import logging

from commands import Command, command_class
from discord import PermissionOverwrite
import file_helper

logger = logging.getLogger(__name__)

faction_commands = {
    "create": 1,
    "remove": 1,
    "help": 0
}

@command_class
class Faction(Command):

    async def handle(self):
        if len(self.args) >= 1:
            # Stop if name is missing.
            if self.args[0] not in faction_commands:
                await self.message.channel.send("`{}` is not a valid faction command.".format(self.args[0]))
            
            else:
                await getattr(self, self.args[0])(*self.args[1:])
        
        # Without any command
        else:
            await self.message.channel.send("Thanks for using the MC-DiscordGroups bot for Factions!\nUse `!faction help` for commands.")


    # Display help menu for factions commands
    async def help(self):
        await self.message.channel.send("No help yet oops")


    # Allow user to create a faction room
    async def create(self, name):
        name = name.lower()
        if not file_helper.faction_exists(name):
            faction_role = await self.guild.create_role(name=name, hoist=False)
            faction_category = await self.guild.create_category_channel(
                name,
                overwrites={
                    faction_role: PermissionOverwrite(read_messages=True, attach_files=True, embed_links=True),
                    self.guild.default_role: PermissionOverwrite(read_messages=False)
                })
            faction_text = await faction_category.create_text_channel("Text Channel")
            faction_voice = await faction_category.create_voice_channel("Voice Channel")

            file_helper.add_faction(name, self.message.author.id, faction_role.id, faction_category.id, faction_text.id, faction_voice.id)
            
            await self.message.author.add_roles(faction_role)
            await self.message.channel.send("Faction created")
        else:
            await self.message.channel.send("A faction with this name already exists.")


    # Allow user to remove a faction room
    async def remove(self, name):
        name = name.lower()
        if file_helper.faction_exists(name):
            faction = file_helper.get_faction(name)
            if self.message.author.id == faction["leader"]:
                deletion_queue = []
                deletion_queue.append(self.guild.get_channel(faction["text_channel"]))
                deletion_queue.append(self.guild.get_channel(faction["voice_channel"]))
                deletion_queue.append(self.guild.get_channel(faction["category_id"]))
                deletion_queue.append(self.guild.get_role(faction["role"]))
                for obj in deletion_queue:
                    if obj:  # Ensure that the channel/role exists before deleting
                        await obj.delete()
                await self.message.channel.send("Faction removed")
                
                file_helper.remove_faction(name)
        else:
            self.message.guild.send("That faction does not exist")
