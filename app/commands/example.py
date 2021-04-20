# !example

from commands import Command, command_class

@command_class
class Example(Command):

    async def handle(self):
        # Immediately return a runt.
        await self.message.channel.send("Example command called!")
