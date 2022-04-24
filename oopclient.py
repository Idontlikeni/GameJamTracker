from turtle import title
import discord
from discord.ext import commands
from discord.utils import get
import random
import requests
from bs4 import BeautifulSoup
import datetime as dt
import logging

link = 'https://itch.io/jams/upcoming/featured'
description = ''''''

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', description=description, intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class GameJamTracker(commands.Cog):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = GameJamTracker()
client.run('my token goes here')

bot.add_cog(GameJamTracker(bot))
