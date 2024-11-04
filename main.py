import discord
from utils.client import Client
from utils.dbhandler import SQLiteHandler
from discord.ext import tasks
import json
from discord import ui, app_commands

# TODO: stuff to handle on start up
with open("secrets.json") as f:
    data = json.load(f)
    token = data['token']

@tasks.loop(seconds = 3) # repeat after every 10 seconds
async def autosave():
    dbhandler.sync()

# Initilize the client and run
intents = discord.Intents.default()
intents.message_content = True
db = {}
dbhandler = SQLiteHandler("ram.sqlite3",db)


client = Client(db,intents,autosave)
bot = app_commands.CommandTree(client)

@app_commands.command(name="gag",description="gag someone >w>")
async def gag(inter:discord.Interaction,mem:discord.Member):
    db['members'][mem.global_name]={'gag':{'t_lvl':'medt'}}
    dbhandler.sync()
    await inter.response.send_message("got gagged")

@app_commands.command(name="ungag",description="ungag someone please >w>")
async def ungag(inter:discord.Interaction,mem:discord.Member):
    db['members'][mem.global_name]=None
    dbhandler.sync()
    await inter.response.send_message("got ungagged")

bot.add_command(gag)
bot.add_command(ungag)

client.set_bot(bot)
client.run(token)