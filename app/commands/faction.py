# !faction <create|remove> (name)

from commands import Command, command_class

faction_commands = [
    "create",
    "remove",
    "help"
]

@command_class
class Faction(Command):

    async def handle(self):
        if len(self.args) >= 1:
            # Stop if name is missing.
            if self.args[0] not in faction_commands:
                await self.message.channel.send("`{}` is not a valid faction command.".format(self.args[0]))
            
            else:
                await getattr(self, self.args[0])()


    # Display help menu for factions commands
    async def help(self):
        await self.message.channel.send("No help yet oops")


    # Allow user to create a faction room
    async def create(self):
        await self.message.channel.send("called create")
        pass


    # Allow user to remove a faction room
    async def remove(self):
        await self.message.channel.send("called remove")
        pass
