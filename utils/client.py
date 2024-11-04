import discord

class Client(discord.Client):
    def __init__(self,intents:discord.Intents,**options):
        super().__init__(intents=intents,**options)

    async def on_message(self,message:discord.Message):
        await message.channel.send("Boops")