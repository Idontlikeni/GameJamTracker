
# This example requires the 'members' privileged intents

from turtle import title
import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import datetime as dt
link = 'https://itch.io/jams/upcoming/featured'
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

role_message_id = 942058070215905341 # ID of the message that can be reacted to to add/remove a role.
emoji_to_role = {
    discord.PartialEmoji(name='1️⃣'): 942069045543456798, # ID of the role associated with unicode emoji '🔴'.
    discord.PartialEmoji(name='2️⃣'): 942070012921933884, # ID of the role associated with unicode emoji '🟡'.
    discord.PartialEmoji(name='3️⃣'): 942070442515116073, # ID of the role associated with unicode emoji '🟡'.
}


def parser(url):
    htm = ''
    games = []
    imgs = []
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    name1 = soup.find_all('div', class_="stat_header_widget")
    soup1 = BeautifulSoup(str(name1[0]), 'lxml')
    name = str(soup1.find_all('h2')[0])
    name = name.split('>')[1].split('<')[0]
    htm += f'<h1>Author: {name}</h1>'
    gms = soup.find_all('a', class_="title game_link")
    for i in gms:
        games.append(i.text)
    im = soup.find_all('div', class_="game_thumb")
    for i in im:
        imgs.append(str(i).split('url(\'')[1].split('\')')[0])
    ln = soup.find_all('a', class_="thumb_link game_link")
    for i in ln:
        links.append(str(i).split('href="')[1].split('"')[0])
    # print(games, links, imgs, sep='\n')
    for i in range(len(games)):
        htm += f'abob{games[i]}\n real shit {links[i]}\n pmg {links[i]}'
    return htm


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
async def gst(ctx):
    names = []
    dates = []
    links = []
    htm = ''
    images = []
    url = 'https://itch.io/jams'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="conversion_link_widget")
    dat = soup.find_all('span', class_="date_countdown")
    imag = soup.find_all('div', class_='jam_cover')
    lin = soup.find_all(['div'], class_="conversion_link_widget")
    for i in imag:
        images.append(str(i).split('data-background_image="')[1].split('"')[0])
    for i in quotes:
        if i.text != '':
            names.append(i.text)
    for i in dat:
        if 'title' in str(i):
            ong = ''
        else:
            ong = 'Ongoing, ends: '
        time = i.text[:-1].split('T')
        datet = list(map(int, time[0].split('-')))
        my_date = dt.date(datet[0], datet[1], datet[-1])
        datet = list(map(int, time[1].split(':')))
        my_time = dt.time(datet[0], datet[1], datet[-1])
        my_datetime = dt.datetime.combine(my_date, my_time)
        delta_time1 = dt.timedelta(hours=3)
        dates.append(ong + str(my_datetime + delta_time1))
    for i in lin:
        links.append(str(i).split('a href="')[1].split('"')[0])
    links = links[::2]
    for i in range(len(names)):
        await ctx.send(f'{names[i]}\n{dates[i]}\nhttps://itch.io{links[i]}')


    # global link
    # """Says when a member joined."""
    # responce = requests.get(link).text
    # soup = BeautifulSoup(responce, 'html.parser')
    # block = soup.find_all('span', class_="date_countdown")
    # for b in block:
    #    await ctx.send('\t'.join(b.text.split('T')))


@bot.command()
async def ust(ctx, profilename: str):
    await ctx.send(parser(f'https://itch.io/profile/{profilename}'))


@bot.command()
async def helpb(ctx):
    embed = discord.Embed(title="Help Command", description='''`/ust <profilename>` - check user profile
    `/gst` - show upcoming gamejams''', colour=0x87CEEB)
    await ctx.send(embed=embed)   


@bot.command()
async def rating(ctx):
    embed = discord.Embed(title="Rating", description='''''', colour=0x87CEEB)
    await ctx.send(embed=embed)   


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.event
async def on_raw_reaction_add(payload):
    
    """Gives a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != role_message_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    try:
        # Finally, add the role.
        await payload.member.add_roles(role)
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass

@bot.event
async def on_raw_reaction_remove(payload):
    """Removes a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != role_message_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    # The payload for `on_raw_reaction_remove` does not provide `.member`
    # so we must get the member ourselves from the payload's `.user_id`.
    member = guild.get_member(payload.user_id)
    print(guild.members, payload.user_id, member)
    if member is None:
        # Make sure the member still exists and is valid.
        return
    try:
        # Finally, remove the role.
        await member.remove_roles(role)
    except discord.HTTPException:
        print('5')
        # If we want to do something in case of errors we'd do it here.
        pass
# ---------------------------------main-------------------------------------------
link = 'https://itch.io/jams/upcoming/featured'
responce = requests.get(link).text
soup = BeautifulSoup(responce, 'html.parser')
#  print(soup.prettify())
# ---------------------------------main-------------------------------------------
bot.run('code')

# import discord

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))

#     async def on_message(self, message):
#         print('Message from {0.author}: {0.content}'.format(message))

# client = MyClient()
# client.run('OTM2OTE2Mzk3NzA2MDY3OTcw.YfUJZA.g4-OmOpRczcQajOfzs86pMvoXMg')