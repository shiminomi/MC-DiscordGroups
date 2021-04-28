# !faction <create|remove> (name)
import logging

from commands import Command, command_class
from discord import PermissionOverwrite
import file_helper

logger = logging.getLogger(__name__)

faction_commands = {
    "create": 1,
    "remove": 1,
    "help": 0,
    "invite": 1,
    "uninvite": 1,
    "accept": 1
}

def is_tag(string):
    return string[:3] == "<@!" and string[-1:] == ">"


@command_class
class Faction(Command):

    async def handle(self):
        if len(self.args) >= 1:
            # Stop if name is missing.
            if self.args[0] not in faction_commands:
                await self.message.channel.send("`{}` is not a valid faction command.".format(self.args[0]))
            
            else:
                # Check if there are valid amount of arguments
                if len(self.args[1:]) == faction_commands[self.args[0]]:
                    await getattr(self, self.args[0])(*self.args[1:])
                else:
                    await self.message.channel.send("Insufficient arguments.")
        
        # Without any command
        else:
            await self.message.channel.send("Thanks for using the MC-DiscordGroups bot for Factions!\nUse `!faction help` for commands.")


    # Display help menu for factions commands
    async def help(self):
        await self.message.channel.send("No help yet oops")


    # Allow user to create a faction room
    async def create(self, faction_name):
        name = faction_name.lower()
        if file_helper.faction_exists(name):
            await self.message.channel.send("A faction with this name already exists.")
            return
    
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


    # Allow user to remove a faction room
    async def remove(self, faction_name):
        name = faction_name.lower()
        if not file_helper.faction_exists(name):
            await self.message.guild.send("That faction does not exist")
            return 

        faction = file_helper.get_faction(name)
        if not self.message.author.id == faction["leader"]:
            await self.message.guild.send("You are not the faction leader!")
            return

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
    

    # Allow user to invite another user
    async def invite(self, member_name):
        faction = file_helper.get_user_faction(self.message.author.id)
        if not faction:
            await self.message.channel.send("You are not in a faction!")
            return

        if not is_tag(member_name):
            await self.message.channel.send("Name invalid, please tag them with @(name) in the command.")
            return

        member_id = int(member_name[3:-1])
        file_helper.add_invite(faction["name"], member_id)


    async def uninvite(self, member_name):
        faction = file_helper.get_user_faction(self.message.author.id)
        if not faction:
            await self.message.channel.send("You are not in a faction!")
            return

        if not is_tag(member_name):
            await self.message.channel.send("Name invalid, please tag them with @(name) in the command.")
            return

        member_id = int(member_name[3:-1])
        file_helper.remove_invite(faction["name"], member_id)


    async def kick(self, member_name):
        faction = file_helper.get_user_faction(self.message.author.id)
        if not self.message.author.id == faction["leader"]:
            await self.message.guild.send("You are not the faction leader!")
            return


    async def accept(self, faction_name):
        pass
