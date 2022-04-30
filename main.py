from turtle import title
import discord
from discord.ext import commands
from discord.utils import get
import random
import requests
from bs4 import BeautifulSoup
import datetime as dt
import asyncio
from discord_components import DiscordComponents, Button, ButtonStyle, ActionRow, ComponentsBot
import logging

link = 'https://itch.io/jams/upcoming/featured'
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
list_len = 5
intents = discord.Intents.all()
intents.members = True
bot = ComponentsBot(command_prefix='.', description=description, intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

data = []
role_message_id = 942058070215905341  # ID of the message that can be reacted to to add/remove a role.
emoji_to_role = {
    discord.PartialEmoji(name='1️⃣'): 942069045543456798,
    # ID of the role associated with unicode emoji '🔴'.
    discord.PartialEmoji(name='2️⃣'): 942070012921933884,
    # ID of the role associated with unicode emoji '🟡'.
    discord.PartialEmoji(name='3️⃣'): 942070442515116073,
    # ID of the role associated with unicode emoji '🟡'.
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
    print(games, links, imgs, sep='\n')
    for i in range(len(games)):
        htm += f'abob{games[i]}\n real shit {links[i]}\n pmg {links[i]}'
    return htm


def top(count: int):
    names = []
    dates = []
    links = []
    images = []
    joined = []
    url = 'https://itch.io/jams'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="conversion_link_widget")
    dat = soup.find_all('span', class_="date_countdown")
    imag = soup.find_all('div', class_='jam_cover')
    lin = soup.find_all(['div'], class_="conversion_link_widget")
    jo = soup.find_all(['div'], class_="stat")
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
    for i in jo:
        joined.append(i.text.split()[0])
    data = []
    for i in range(len(names)):
        data.append(
            (names[i], dates[i], links[i], images[i], int(''.join(joined[i].split(',')))))
    for i in data:
        if 'Ongoing' in i[1]:
            data.remove(i)
    data = sorted(data, key=lambda student: student[-1])
    data.reverse()
    data = data[:count]
    for i in data:
        print(i)
    return data


async def timer(name, date, context, delta):
    i = 0
    while True:
        msg = await context.fetch_message(role_message_id)
        arr = top(list_len)
        await msg.edit(content='\n'.join([f"{i + 1} - {arr[i][0]}" for i in range(list_len)]))
        i += 1
        await asyncio.sleep(delta)


async def update_data():
    global data
    names = []
    dates = []
    links = []
    images = []
    joined = []
    url = 'https://itch.io/jams'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="conversion_link_widget")
    dat = soup.find_all('span', class_="date_countdown")
    imag = soup.find_all('div', class_='jam_cover')
    lin = soup.find_all(['div'], class_="conversion_link_widget")
    jo = soup.find_all(['div'], class_="stat")
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
    for i in jo:
        joined.append(i.text.split()[0])
    data = []
    for i in range(len(names)):
        data.append((names[i], dates[i], links[i], images[i], int(''.join(joined[i].split(',')))))


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
    global data
    jam = 0
    await update_data()
    #  print(data)
    data1 = data[jam]
    msg = await ctx.send(
        embed=discord.Embed(title=data1[0], description=f'Date: {data1[1]} \n Joined: {data1[-1]}').set_image(
            url=data1[3]),
        components=[ActionRow(Button(style=ButtonStyle.blue, label='Previous', custom_id='prev'),
                              Button(style=ButtonStyle.URL, label='url', url=f'https://itch.io{data1[2]}',
                                     custom_id='lin'),
                              Button(style=ButtonStyle.green, label='Next', custom_id='nex'))
                    ]
    )
    while True:
        response = await bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.component.label == 'Next':
                jam += 1
                if jam == len(data):
                    jam = 0
            if response.component.label == 'Previous':
                jam -= 1
                if jam == -1:
                    jam = len(data) - 1
        data1 = data[jam]
        await msg.edit(embed=discord.Embed(title=data1[0],
                                           description=f'Date: {data1[1]} \n Joined: {data1[-1]}').set_image(
            url=data1[3]),
            components=[ActionRow(Button(style=ButtonStyle.blue, label='Previous', custom_id='prev'),
                                  Button(style=ButtonStyle.URL, label='url',
                                         url=f'https://itch.io{data1[2]}', custom_id='lin'),
                                  Button(style=ButtonStyle.green, label='Next', custom_id='nex'))
                        ])
        try:
            await response.respond()
            print('b')
        except:
            print('c')
            pass

    # global link
    # """Says when a member joined."""
    # responce = requests.get(link).text
    # soup = BeautifulSoup(responce, 'html.parser')
    # block = soup.find_all('span', class_="date_countdown")
    # for b in block:
    #    await ctx.send('\t'.join(b.text.split('T')))


@bot.command()
async def ust(ctx, *profilename: str):
    # await ctx.send(parser(f'https://itch.io/profile/{profilename}'))
    profilename = '-'.join(profilename).lower()
    jam = 0
    data = []
    games = []
    imgs = []
    links = []
    stats = []
    response = requests.get(f'https://itch.io/profile/{profilename}')
    soup = BeautifulSoup(response.text, 'lxml')
    name1 = soup.find_all('div', class_="stat_header_widget")
    soup1 = BeautifulSoup(str(name1[0]), 'lxml')
    name = str(soup1.find_all('h2')[0])
    name = name.split('>')[1].split('<')[0]
    gms = soup.find_all('a', class_="title game_link")
    statiscs = soup.find_all('div', class_="stat_box")
    ava = str(soup.find_all('div', class_="avatar")[0]).split("url('")[1].split("')")[0]
    print(ava)
    rg = soup.find_all('abbr')
    stats.append(f'Registration date {rg[0].text}')
    for i in gms:
        games.append(i.text)
    im = soup.find_all('div', class_="game_thumb")
    for i in im:
        imgs.append(str(i).split('url(\'')[1].split('\')')[0])
    ln = soup.find_all('a', class_="thumb_link game_link")
    for i in ln:
        links.append(str(i).split('href="')[1].split('"')[0])
    for i in statiscs:
        i = str(i).split('</div><div class="stat_label">')
        stats.append(i[0].split('>')[-1] + ' ' + i[1].split('<')[0])
    print(name)
    print(stats)
    for i in range(len(games)):
        data.append([games[i], imgs[i], links[i]])
    print(data)
    stat = ''
    for i in range(len(stats)):
        if i == 0:
            stat += stats[0]
        elif i == 1:
            stat += f'\nPosts: {stats[1]}'
        elif i == 2:
            stat += f'\nTopics: {stats[2]}'
        elif i == 3:
            stat += f'\nFollowers: {stats[3]}'
        elif i == 4:
            stat += f'\nPeople is followed: {stats[4]}'
    stat += f'\nGames: {len(games)} games'
    shgm = 'components=['
    for i in data:
        s = i
        shgm += f"embed=discord.Embed(title='{s[0]}', description='{s[2]}'), "
    shgm += ']'
    print(shgm)
    if games:
        await ctx.send(
            embed=discord.Embed(title=name, description=stat).set_image(
                url=ava),
            components=[ActionRow(
                Button(style=ButtonStyle.URL, label='Profile', url=f'https://itch.io/profile/{profilename}',
                       custom_id='lin'),
                Button(style=ButtonStyle.URL, label='Creator page', url=f'https://{profilename}.itch.io',
                       custom_id='lin'),
                Button(style=ButtonStyle.green, label='Show games', custom_id='nex'))])
        response = await bot.wait_for("button_click")
        msg = await response.send(embed=discord.Embed(title=data[0][0], description=data[0][2]).set_image(
                url=data[0][1]),
                components=[ActionRow(Button(style=ButtonStyle.blue, label='Previous', custom_id='prev'),
                                      Button(style=ButtonStyle.URL, label='Link',
                                             url=f'{data[0][2]}', custom_id='lin'),
                                      Button(style=ButtonStyle.green, label='Next', custom_id='nex'))
                            ])
        print(msg.id)
        while True:
            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.label == 'Next':
                    jam += 1
                    if jam == len(data):
                        jam = 0
                if response.component.label == 'Previous':
                    jam -= 1
                    if jam == -1:
                        jam = len(data) - 1
            data1 = data[jam]
            print(data1[1])
            await msg.edit(embed=discord.Embed(title=data1[0], description=data1[2]).set_image(
                url=data1[1]),
                components=[ActionRow(Button(style=ButtonStyle.blue, label='Previous', custom_id='prev'),
                                      Button(style=ButtonStyle.URL, label='Link',
                                             url=f'https://itch.io{data1[1]}', custom_id='lin'),
                                      Button(style=ButtonStyle.green, label='Next', custom_id='nex'))
                            ])
            try:
                await response.respond()
            except:
                pass
    else:
        await ctx.send(
            embed=discord.Embed(title=name, description=stat).set_image(
                url=ava),
            components=[ActionRow(
                Button(style=ButtonStyle.URL, label='Profile', url=f'https://itch.io/profile/{profilename}',
                       custom_id='lin'),
                Button(style=ButtonStyle.URL, label='Creator page', url=f'https://{profilename}.itch.io',
                       custom_id='lin'))])


@bot.command()
async def start_timer(ctx):
    await asyncio.gather(
        asyncio.create_task(timer("test", "sadasda", ctx, 10)))


@bot.command()
async def helpb(ctx):
    embed = discord.Embed(title="Help Command", description='''`/ust <profilename>` - check user profile
    `/gst` - show upcoming gamejams''', colour=0x87CEEB)
    await ctx.send(embed=embed)


@bot.command()
async def rating(ctx):
    embed = discord.Embed(title="Rating", description='''''', colour=0x87CEEB)
    await ctx.send(embed=embed)


@bot.command()
async def set_message_id(ctx, msg_id: int):
    global role_message_id
    role_message_id = msg_id
    await asyncio.gather(
        asyncio.create_task(timer("test", "sadasda", ctx, 10)))


@bot.command()
async def write_top(ctx, num: int):
    global list_len
    await ctx.send('\n'.join([f"{i + 1} - " for i in range(num)]))
    list_len = num


@bot.command()
async def add_role(ctx, emoji, role_id: int):
    emoji_to_role[discord.PartialEmoji(name=emoji)] = role_id
    print(f'{emoji} set to {get(ctx.guild.roles, id=role_id)}')


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
    print(payload.message_id, role_message_id)

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
bot.run('OTY0MTA3MzY4NDc0NTA5MzUy.Ylf09A.kzbk9J2kSQRD9KQfarww0XNSLF8')
