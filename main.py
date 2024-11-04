import discord
from utils.client import Client
import json

# TODO: stuff to handle on start up
with open("secrets.json") as f:
    data = json.load(f)
    token = data['token']

# Initilize the client and run
intents = discord.Intents.default()
intents.messages = True

client = Client(intents=intents)
client.run(token)