# from turtle import title
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
import sqlite3

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
response_id = 0
response_id_timer = 0
data = []
fdata = []
roles_dct = dict()
roles_dct_num = dict()
role_message_id = 942058070215905341  # ID of the message that can be reacted to to add/remove a
# role.
blue_color = 0x87CEEB
purple_color = 0xf954f6
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
emoji_to_role = dict()


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
            ong = False
        else:
            ong = True
        time = i.text[:-1].split('T')
        datet = list(map(int, time[0].split('-')))
        my_date = dt.date(datet[0], datet[1], datet[-1])
        datet = list(map(int, time[1].split(':')))
        my_time = dt.time(datet[0], datet[1], datet[-1])
        my_datetime = dt.datetime.combine(my_date, my_time)
        delta_time1 = dt.timedelta(hours=3)
        dates.append((ong, my_datetime + delta_time1))
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
    data = sorted(data, key=lambda student: student[1])
    #  data.reverse()
    data = data[:count]
    #  for i in data:
    #  print(i)
    return data


def check(n):
    if n:
        return 'Ongoing, '
    else:
        return ''


async def timer(name, date, context, delta):
    i = 0
    while True:
        msg = await context.fetch_message(role_message_id)
        arr = top(list_len)
        await msg.edit(content='\n'.join(
            [f"{j + 1} - {arr[j][0]}(" + check(arr[j][1][0]) + " Date: " + str(arr[j][1][1]) + " )"
             for j in range(list_len)]))
        for j in range(list_len):
            print(arr[j][0], arr[j][1][1] - dt.datetime.now())
            delt = arr[j][1][1] - dt.datetime.now()
            print(delt, type(delt))
            if delt.days < 0 and delt.hours <= 1:
                await context.send(f"@{roles_dct_num[j]} your jam starts soon!")
        #  print(arr[i][1], dt.datetime.now(), arr[i][1][1] - dt.datetime.now(), sep='|')
        i += 1
        await asyncio.sleep(delta)


async def timer_to_future(name, ctx, jam_time, response, img, link):
    # await ctx.send(f'Таймер успешно установлен.')
    while True:
        if jam_time < dt.datetime.now():
            # await ctx.send(f'{ctx.author.mention}, Джем {name} начался.')
            # await response.respond(content=f'{ctx.author.mention}, Джем {name} начался.')
            await response.reply(f'{ctx.author.mention}',
                                 embed=discord.Embed(title='⚠Уведомление⚠',
                                                     description=f'Джем {name} начался.').set_image(
                                     url=img),
                                 components=[
                                     ActionRow(Button(style=ButtonStyle.URL, label='Link',
                                                      url=f'https://itch.io{link}',
                                                      custom_id='lin'))])
            break
        await asyncio.sleep(300)


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


async def update_fdata():
    global fdata
    names = []
    dates = []
    dates1 = []
    deltime = []
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
        dates1.append(my_datetime + delta_time1)
        deltime.append(my_datetime + delta_time1 - dt.datetime.now())
    for i in lin:
        links.append(str(i).split('a href="')[1].split('"')[0])
    links = links[::2]
    for i in jo:
        joined.append(i.text.split()[0])
    fdata = []
    for i in range(len(names)):
        fdata.append(
            (names[i], dates[i], dates1[i], deltime[i], links[i], images[i],
             int(''.join(joined[i].split(',')))))
    fdata = list(filter(lambda x: 'Ongoing, ends:' not in x[1], fdata))
    fdata = sorted(fdata, key=lambda x: x[2])
    print(fdata)


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
async def lust(ctx, *name):
    name = ' '.join(name)
    con = sqlite3.connect('statistic/statistics.db')
    cur = con.cursor()
    score = cur.execute(f"""SELECT score FROM stats WHERE user == '{name}'""").fetchall()
    total = cur.execute(f"""SELECT total_games FROM stats WHERE
                         user == '{name}'""").fetchall()
    win = cur.execute(f"""SELECT win_games FROM stats WHERE
                         user == '{name}'""").fetchall()
    chat = cur.execute(f"""SELECT chat_help FROM stats WHERE
                         user == '{name}'""").fetchall()
    timers = cur.execute(f"""SELECT timers_added FROM stats WHERE
                         user == '{name}'""").fetchall()
    con.commit()
    con.close()
    if score:
        await ctx.reply('💥Статистика💥',
                        embed=discord.Embed(title=f'Статистика пользователя: `{name}`:',
                                            description=f'Всего очков: {score[0][0]}\nИгр сыграно: '
                                                        f'{total[0][0]}\n '
                                                        f'Игр выигрыно: {win[0][0]}\n'
                                                        f'Помощей в чате: {chat[0][0]}\n'
                                                        f'Добавлено таймеров: {timers[0][0]}',
                                            colour=purple_color))
    else:
        await ctx.reply('💥Статистика💥',
                        embed=discord.Embed(title=f'⚠Внимание⚠',
                                            description=f'❌Пользаватель `{name}` не найден❌',
                                            colour=purple_color))


@bot.command()
async def games(ctx):
    msg = await ctx.send('Выбор мини-игры:',
                         embed=discord.Embed(title='Все мини-игры:',
                                             description=f'1️⃣Случайное число.\n\nПростой '
                                                         f'рандомайзер чисел от 1 до '
                                                         f' 100.\n\n--------------------\n\n2'
                                                         f'️⃣Кости.\n\nБот подбросит '
                                                         f' специально для вас 2 игральные кости. '
                                                         f'Сколько на них '
                                                         f' выпадет?\n\n-------------------\n\n3'
                                                         f'️⃣Угадай число.\n\nБот '
                                                         f' загадает число от 1 до 10. Ваша задача '
                                                         f'- угадать его. '
                                                         f' Сможете ли вы? Ваши шансы на успех '
                                                         f'равны 10%.',
                                             colour=purple_color),
                         components=[
                             ActionRow(Button(style=ButtonStyle.grey, label='1️⃣Случайное число',
                                              custom_id='g1'),
                                       Button(style=ButtonStyle.grey, label='2️⃣Кости',
                                              custom_id='g2'),
                                       Button(style=ButtonStyle.grey, label='3️⃣Угадай число',
                                              custom_id='g3'))
                         ],
                         )
    response = await bot.wait_for("button_click")
    if response.channel == ctx.channel:
        if response.component.custom_id == 'g1':
            await response.respond(embed=discord.Embed(title="🎮Мини-игра Случайное число🎰",
                                                       description=f'Простой рандомайзер чисел от '
                                                                   f'1 до 100. '
                                                                   f'\n\nВы хотите начать игру?',
                                                       colour=blue_color),
                                   components=[
                                       ActionRow(Button(style=ButtonStyle.grey, label='Да✅',
                                                        custom_id='yes1'),
                                                 Button(style=ButtonStyle.grey, label='Нет❌',
                                                        custom_id='no1'))
                                   ],
                                   )
            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.custom_id == 'yes1':
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Случайное число🎰",
                                                               description=f'Бот загадал число'
                                                                f' ✨ `{random.randint(1, 100)}` ✨',
                                                               colour=purple_color)
                                           )
                    con = sqlite3.connect('statistic/statistics.db')
                    cur = con.cursor()
                    score = cur.execute(
                        f"""SELECT score FROM stats WHERE user == '{response.author}'""").fetchall()
                    rnd_games = cur.execute(f"""SELECT rnd FROM stats WHERE
                     user == '{response.author}'""").fetchall()
                    con.commit()
                    con.close()
                    # print(score)
                    if not score:
                        con = sqlite3.connect('statistic/statistics.db')
                        cur = con.cursor()
                        score = cur.execute(
                            f"""INSERT INTO stats(user, score, rnd, total_games, win_games, cube, 
                        chat_help, timers_added) VALUES('{response.author}', 1, 1, 0, 0, 0, 0, 0)""").fetchall()
                        con.commit()
                        con.close()
                    else:
                        con = sqlite3.connect('statistic/statistics.db')
                        cur = con.cursor()
                        score = cur.execute(f"""UPDATE stats SET score = {score[0][0] + 1}
                        where user = '{response.author}'""").fetchall()
                        score = cur.execute(f"""UPDATE stats SET rnd = {rnd_games[0][0] + 1}
                                                where user = '{response.author}'""").fetchall()
                        con.commit()
                        con.close()
                if response.component.custom_id == 'no1':
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Случайное число🎰",
                                                               description=f'❌Игра окончена.❌',
                                                               colour=purple_color)
                                           )
        if response.component.custom_id == 'g2':
            await response.respond(embed=discord.Embed(title="🎮Мини-игра Кости🎲",
                                                       description=f'Бот подбросит'
                                                                   f' специально для вас 2 игральные кости. Сколько'
                                                                   f' на них выпадет?'
                                                                   f'\n\nВы хотите начать игру?',
                                                       colour=blue_color),
                                   components=[
                                       ActionRow(Button(style=ButtonStyle.grey, label='Да✅',
                                                        custom_id='yes2'),
                                                 Button(style=ButtonStyle.grey, label='Нет❌',
                                                        custom_id='no2'))
                                   ],
                                   )
            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.custom_id == 'yes2':
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Кости🎲",
                                                               description=f'Бот подбрасывает кости'
                                                                           f' ⚡ `{random.choice(dashes)}` ⚡'
                                                                           f' `{random.choice(dashes)}` ⚡',
                                                               colour=purple_color)
                                           )
                    con = sqlite3.connect('statistic/statistics.db')
                    cur = con.cursor()
                    score = cur.execute(
                        f"""SELECT score FROM stats WHERE user == '{response.author}'""").fetchall()
                    cube = cur.execute(f"""SELECT cube FROM stats WHERE
                                         user == '{response.author}'""").fetchall()
                    con.commit()
                    con.close()
                    # print(score)
                    if not score:
                        con = sqlite3.connect('statistic/statistics.db')
                        cur = con.cursor()
                        score = cur.execute(
                            f"""INSERT INTO stats(user, score, rnd, total_games, win_games, cube, 
                                            chat_help, timers_added) 
                                            VALUES('{response.author}', 1, 0, 0, 0, 1, 0, 0)""").fetchall()
                        con.commit()
                        con.close()
                    else:
                        con = sqlite3.connect('statistic/statistics.db')
                        cur = con.cursor()
                        score = cur.execute(f"""UPDATE stats SET score = {score[0][0] + 1}
                                            where user = '{response.author}'""").fetchall()
                        score = cur.execute(f"""UPDATE stats SET cube = {cube[0][0] + 1}
                                                                    where user = '{response.author}'""").fetchall()
                        con.commit()
                        con.close()
                if response.component.custom_id == 'no2':
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Кости🎲",
                                                               description=f'❌Игра окончена.❌',
                                                               colour=purple_color)
                                           )
        if response.component.custom_id == 'g3':
            await response.respond(embed=discord.Embed(title="🎮Мини-игра Угадай число🔮",
                                                       description=f'Бот'
                                                                   f' загадает число от 1 до 10. Ваша задача'
                                                                   f' - угадать его. Сможете ли вы? Ваши шансы'
                                                                   f' на успех равны 10%.'
                                                                   f'\n\nВы хотите начать игру?',
                                                       colour=blue_color),
                                   components=[
                                       ActionRow(Button(style=ButtonStyle.grey, label='Да✅',
                                                        custom_id='yes3'),
                                                 Button(style=ButtonStyle.grey, label='Нет❌',
                                                        custom_id='no3'))
                                   ],
                                   )
            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.custom_id == 'yes3':
                    num = random.randint(1, 10)
                    print('num', num)
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Угадай число🔮",
                                                               description=f'Бот загадал число. Пожалуйста,'
                                                                           f' выберите число.',
                                                               colour=purple_color),
                                           components=[
                                               ActionRow(Button(style=ButtonStyle.grey, label='1️⃣',
                                                                custom_id='n1'),
                                                         Button(style=ButtonStyle.grey, label='2️⃣',
                                                                custom_id='n2'),
                                                         Button(style=ButtonStyle.grey, label='3️⃣',
                                                                custom_id='n3'),
                                                         Button(style=ButtonStyle.grey, label='4️⃣',
                                                                custom_id='n4'),
                                                         Button(style=ButtonStyle.grey, label='5️⃣',
                                                                custom_id='n5')),
                                               ActionRow(Button(style=ButtonStyle.grey, label='6️⃣',
                                                                custom_id='n6'),
                                                         Button(style=ButtonStyle.grey, label='7️⃣',
                                                                custom_id='n7'),
                                                         Button(style=ButtonStyle.grey, label='8️⃣',
                                                                custom_id='n8'),
                                                         Button(style=ButtonStyle.grey, label='9️⃣',
                                                                custom_id='n9'),
                                                         Button(style=ButtonStyle.grey, label='🔟',
                                                                custom_id='n10'))
                                           ]
                                           )
                    response = await bot.wait_for("button_click")
                    if response.channel == ctx.channel:
                        if response.component.custom_id == 'n' + str(num):
                            await response.respond(
                                embed=discord.Embed(title="🎮Мини-игра Угадай число🔮",
                                                    description=f'🔥Всё верно!🔥 Бот загадал число'
                                                                f' 💫 `{num}` 💫',
                                                    colour=blue_color)
                            )
                            con = sqlite3.connect('statistic/statistics.db')
                            cur = con.cursor()
                            score = cur.execute(
                                f"""SELECT score FROM stats WHERE user == '{response.author}'""").fetchall()
                            win = cur.execute(f"""SELECT win_games FROM stats WHERE
                                                 user == '{response.author}'""").fetchall()
                            total = cur.execute(f"""SELECT total_games FROM stats WHERE
                                                                             user == '{response.author}'""").fetchall()
                            con.commit()
                            con.close()
                            # print(score)
                            if not score:
                                con = sqlite3.connect('statistic/statistics.db')
                                cur = con.cursor()
                                score = cur.execute(
                                    f"""INSERT INTO stats(user, score, rnd, total_games, win_games,
                                 cube, chat_help, timers_added) 
                                 VALUES('{response.author}', 20, 0, 1, 1, 0, 0, 0)""").fetchall()
                                con.commit()
                                con.close()
                            else:
                                con = sqlite3.connect('statistic/statistics.db')
                                cur = con.cursor()
                                score = cur.execute(f"""UPDATE stats SET score = {score[0][0] + 20}
                                                    where user = '{response.author}'""").fetchall()
                                score = cur.execute(
                                    f"""UPDATE stats SET total_games = {total[0][0] + 1}
                                                    where user = '{response.author}'""").fetchall()
                                score = cur.execute(f"""UPDATE stats SET win_games = {win[0][0] + 1}
                                                    where user = '{response.author}'""").fetchall()
                                con.commit()
                                con.close()
                        else:
                            await response.respond(
                                embed=discord.Embed(title="🎮Мини-игра Угадай число🔮",
                                                    description=f'❌К сожалению вы не правы.❌ Бот '
                                                                f'загадал число 💫 `{num}` 💫',
                                                    colour=blue_color)
                            )
                            con = sqlite3.connect('statistic/statistics.db')
                            cur = con.cursor()
                            score = cur.execute(
                                f"""SELECT score FROM stats WHERE user == '{response.author}'""").fetchall()
                            win = cur.execute(f"""SELECT win_games FROM stats WHERE
                                                                             user == '{response.author}'""").fetchall()
                            total = cur.execute(f"""SELECT total_games FROM stats WHERE
                                                                            user == '{response.author}'""").fetchall()
                            con.commit()
                            con.close()
                            # print(score)
                            if not score:
                                con = sqlite3.connect('statistic/statistics.db')
                                cur = con.cursor()
                                score = cur.execute(
                                    f"""INSERT INTO stats(user, score, rnd, total_games, win_games,
                                                    cube, chat_help, timers_added) 
                                                    VALUES('{response.author}', 1, 0, 1, 0, 0, 0, 0)""").fetchall()
                                con.commit()
                                con.close()
                            else:
                                con = sqlite3.connect('statistic/statistics.db')
                                cur = con.cursor()
                                score = cur.execute(f"""UPDATE stats SET score = {score[0][0] + 1}
                                                                        where user = '{response.author}'""").fetchall()
                                score = cur.execute(
                                    f"""UPDATE stats SET total_games = {total[0][0] + 1}
                                                                        where user = '{response.author}'""").fetchall()
                                con.commit()
                                con.close()
                if response.component.custom_id == 'no3':
                    await response.respond(embed=discord.Embed(title="🎮Мини-игра Угадай число🔮",
                                                               description=f'❌Игра окончена.❌',
                                                               colour=purple_color)
                                           )


@bot.command()
async def gst(ctx):
    global data
    jam = 0
    await update_data()
    #  print(data)
    data1 = data[jam]
    msg = await ctx.send('All jams:',
                         embed=discord.Embed(title=data1[0],
                                             description=f'Date: {data1[1]} \n Joined: {data1[-1]}').set_image(
                             url=data1[3]),
                         components=[ActionRow(
                             Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='prev'),
                             Button(style=ButtonStyle.URL, label='Link',
                                    url=f'https://itch.io{data1[2]}',
                                    custom_id='lin'),
                             Button(style=ButtonStyle.green, label='Next🡲', custom_id='nex'))
                         ]
                         )
    while True:
        response = await bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.component.custom_id == 'nex':
                jam += 1
                if jam == len(data):
                    jam = 0
            if response.component.custom_id == 'prev':
                jam -= 1
                if jam == -1:
                    jam = len(data) - 1
        data1 = data[jam]
        await msg.edit('All jams:', embed=discord.Embed(title=data1[0],
                                                        description=f'Date: {data1[1]} \n Joined: {data1[-1]}').set_image(
            url=data1[3]),
                       components=[ActionRow(
                           Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='prev'),
                           Button(style=ButtonStyle.URL, label='Link',
                                  url=f'https://itch.io{data1[2]}', custom_id='lin'),
                           Button(style=ButtonStyle.green, label='Next🡲', custom_id='nex'))
                       ])
        try:
            await response.respond()
            # print('b')
        except:
            # print('c')
            pass

    # global link
    # """Says when a member joined."""
    # responce = requests.get(link).text
    # soup = BeautifulSoup(responce, 'html.parser')
    # block = soup.find_all('span', class_="date_countdown")
    # for b in block:
    #    await ctx.send('\t'.join(b.text.split('T')))


@bot.command()
async def future_jams(ctx):
    global fdata
    await update_fdata()
    jam = 0
    data = fdata
    #  print(data)
    data1 = data[jam]
    msg = await ctx.send('Future jams:',
                         embed=discord.Embed(title=data1[0],
                                             description=f'Date: {data1[1]} \nTime to: {data1[3].days} days {data1[3].seconds // 3600} hours \nJoined: {data1[-1]}').set_image(
                             url=data1[5]),
                         components=[ActionRow(
                             Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='fprev'),
                             Button(style=ButtonStyle.URL, label='Link',
                                    url=f'https://itch.io{data1[4]}',
                                    custom_id='lin'),
                             Button(style=ButtonStyle.red, label='Set timer', custom_id='ftim'),
                             Button(style=ButtonStyle.green, label='Next🡲', custom_id='fnex'))
                         ]
                         )
    while True:
        response = await bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.component.custom_id == 'fnex':
                jam += 1
                if jam == len(data):
                    jam = 0
            if response.component.custom_id == 'fprev':
                jam -= 1
                if jam == -1:
                    jam = len(data) - 1
            if response.component.custom_id == 'ftim':
                response = await response.respond(
                    embed=discord.Embed(title='⚠Уведомление⚠',
                                        description=f'Таймер на {data1[0]} успешно установлен').set_image(
                        url=data1[5]),
                    components=[ActionRow(
                        Button(style=ButtonStyle.URL, label='Link', url=f'https://itch.io{data1[4]}',
                               custom_id='lin'))])
                await asyncio.gather(asyncio.create_task(
                    timer_to_future(data1[0], ctx, data1[2], msg,
                                    data1[5], data1[4])))
                # await asyncio.gather(asyncio.create_task(
                #     timer_to_future(data1[0], ctx, data1[2] - dt.timedelta(days=11, hours=7, minutes=15), msg,
                #                     data1[5], data1[4])))
                return
        data1 = data[jam]
        await msg.edit('Future jams:', embed=discord.Embed(title=data1[0],
                                                           description=f'Date: {data1[1]} \nTime to: {data1[3].days} days {data1[3].seconds // 3600} hours \nJoined: {data1[-1]}').set_image(
            url=data1[5]),
                       components=[ActionRow(
                           Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='fprev'),
                           Button(style=ButtonStyle.URL, label='Link',
                                  url=f'https://itch.io{data1[4]}', custom_id='lin'),
                           Button(style=ButtonStyle.red, label='Set timer', custom_id='ftim'),
                           Button(style=ButtonStyle.green, label='Next🡲', custom_id='fnex'))
                       ])
        try:
            await response.respond()
            # print('b')
        except:
            # print('c')
            pass


@bot.command()
async def fst(ctx):
    global fdata
    await update_fdata()
    jam = 0
    data = fdata
    #  print(data)
    data1 = data[jam]
    msg = await ctx.send('Future jams:',
                         embed=discord.Embed(title=data1[0],
                                             description=f'Date: {data1[1]} \nTime to: {data1[3].days} days'
                                                         f' {data1[3].seconds // 3600} hours \nJoined: {data1[-1]}',
                                             colour=blue_color).set_image(
                             url=data1[5]),
                         components=[ActionRow(
                             Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='fprev'),
                             Button(style=ButtonStyle.green, label='Next🡲', custom_id='fnex')),
                             ActionRow(Button(style=ButtonStyle.URL, label='Link',
                                              url=f'https://itch.io{data1[4]}',
                                              custom_id='lin'),
                                       Button(style=ButtonStyle.red, label='Set timer',
                                              custom_id='ftim'))
                         ]
                         )
    while True:
        response = await bot.wait_for("button_click")
        print(1, response)
        auth = response.author
        if response.channel == ctx.channel:
            if response.component.custom_id == 'fnex':
                jam += 1
                if jam == len(data):
                    jam = 0
            if response.component.custom_id == 'fprev':
                jam -= 1
                if jam == -1:
                    jam = len(data) - 1
            if response.component.custom_id == 'ftim':
                await response.respond(
                    embed=discord.Embed(title='⚠Уведомление⚠',
                                        description=f"Таймер на `{data1[0]}` успешно установлен",
                                        colour=purple_color).set_image(url=data1[5]),
                    components=[ActionRow(
                        Button(style=ButtonStyle.URL, label='Link', url=f'https://itch.io{data1[4]}',
                               custom_id='lin'))])
                con = sqlite3.connect('statistic/statistics.db')
                cur = con.cursor()
                score = cur.execute(
                    f"""SELECT score FROM stats WHERE user == '{response.author}'""").fetchall()
                timers = cur.execute(f"""SELECT timers_added FROM stats WHERE
                                     user == '{response.author}'""").fetchall()
                con.commit()
                con.close()
                # print(score)
                if not score:
                    con = sqlite3.connect('statistic/statistics.db')
                    cur = con.cursor()
                    score = cur.execute(
                        f"""INSERT INTO stats(user, score, rnd, total_games, win_games, cube, 
                                        chat_help, timers_added) 
                                        VALUES('{response.author}', 1, 0, 0, 0, 0, 0, 1)""").fetchall()
                    con.commit()
                    con.close()
                else:
                    con = sqlite3.connect('statistic/statistics.db')
                    cur = con.cursor()
                    score = cur.execute(f"""UPDATE stats SET score = {score[0][0] + 1}
                                        where user = '{response.author}'""").fetchall()
                    score = cur.execute(f"""UPDATE stats SET timers_added = {timers[0][0] + 1}
                                                                where user = '{response.author}'""").fetchall()
                    con.commit()
                    con.close()
                await asyncio.gather(asyncio.create_task(
                    timer_to_future(data1[0], ctx, data1[2], msg,
                                    data1[5], data1[4], auth)))
                # print(2, response)
                # await asyncio.gather(asyncio.create_task(
                #     timer_to_future(data1[0], ctx, data1[2] - dt.timedelta(days=11, hours=7, minutes=15), msg,
                #                     data1[5], data1[4], auth)))
                return
        data1 = data[jam]
        await msg.edit('Future jams:', embed=discord.Embed(title=data1[0],
                                                           description=f'Date: {data1[1]} \nTime to: {data1[3].days}'
                                                                       f' days {data1[3].seconds // 3600} hours'
                                                                       f' \nJoined: {data1[-1]}',
                                                           colour=blue_color).set_image(
            url=data1[5]),
                       components=[ActionRow(
                           Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='fprev'),
                           Button(style=ButtonStyle.green, label='Next🡲', custom_id='fnex')),
                           ActionRow(Button(style=ButtonStyle.URL, label='Link',
                                            url=f'https://itch.io{data1[4]}',
                                            custom_id='lin'),
                                     Button(style=ButtonStyle.red, label='Set timer',
                                            custom_id='ftim'))
                       ])
        try:
            await response.respond()
            # print('b')
        except:
            # print('c')
            pass


@bot.command()
async def ust(ctx, *profilename: str):
    # await ctx.send(parser(f'https://itch.io/profile/{profilename}'))
    global response_id
    response_id += 1
    id = response_id
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
    if '/static/images/' in ava:
        ava = 'https://itch.io/' + ava
    #  print('ava', ava)
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
    #  print(name)
    #  print(stats)
    for i in range(len(games)):
        data.append([games[i], imgs[i], links[i]])
    #  print(data)
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
    #  print(shgm)
    if response_id == id:
        if games:
            await ctx.send(
                embed=discord.Embed(title=name, description=stat).set_image(
                    url=ava),
                components=[ActionRow(
                    Button(style=ButtonStyle.URL, label='Profile',
                           url=f'https://itch.io/profile/{profilename}',
                           custom_id='lin'),
                    Button(style=ButtonStyle.URL, label='Creator page',
                           url=f'https://{profilename}.itch.io',
                           custom_id='lin'),
                    Button(style=ButtonStyle.green, label='Show games', custom_id='nex'))])
            response = await bot.wait_for("button_click")
            #  print(response)
            if response_id == id:
                msg = await ctx.send(embed=discord.Embed(title=data[0][0]).set_image(
                    url=data[0][1]),
                    components=[ActionRow(
                        Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='prev'),
                        Button(style=ButtonStyle.URL, label='Link',
                               url=data[0][2], custom_id='lin'),
                        Button(style=ButtonStyle.green, label='Next🡲', custom_id='nex'))
                    ])
                try:
                    await response.respond()
                except:
                    pass
                #  print(msg.id)
                while True:
                    #  print(id, response_id)
                    if response_id > id:
                        break
                    response = await bot.wait_for("button_click")
                    if response.channel == ctx.channel:
                        if response.component.label == 'Next🡲':
                            jam += 1
                            if jam == len(data):
                                jam = 0
                        if response.component.label == '🡰Previous':
                            jam -= 1
                            if jam == -1:
                                jam = len(data) - 1
                    data1 = data[jam]
                    #  print(data1, jam)
                    #  print(data1[1])
                    #  print(data[1][1])
                    #  print(data[0][1])
                    await msg.edit(embed=discord.Embed(title=data1[0]).set_image(
                        url=data1[1]),
                        components=[ActionRow(
                            Button(style=ButtonStyle.blue, label='🡰Previous', custom_id='prev'),
                            Button(style=ButtonStyle.URL, label='Link',
                                   url=data1[2], custom_id='lin'),
                            Button(style=ButtonStyle.green, label='Next🡲', custom_id='nex'))
                        ])
                    try:
                        await response.respond()
                    except:
                        pass
                    print()
            else:
                return
        else:
            await ctx.send(
                embed=discord.Embed(title=name, description=stat).set_image(
                    url=ava),
                components=[ActionRow(
                    Button(style=ButtonStyle.URL, label='Profile',
                           url=f'https://itch.io/profile/{profilename}',
                           custom_id='lin'),
                    Button(style=ButtonStyle.URL, label='Creator page',
                           url=f'https://{profilename}.itch.io',
                           custom_id='lin'))])
            return


@bot.command()
async def start_timer(ctx):
    await asyncio.gather(
        asyncio.create_task(timer("test", "sadasda", ctx, 30)))


@bot.command()
async def helpb(ctx):
    embed = discord.Embed(title="❔Help Command", description='''`.ust <profilename>` - check user profile
     from itch.io
     \n`.lust <profilename>` - check user profile from local bot data
     \n`.gst` - show all gamejams
     \n`.fst` - show upcoming gamejams\n`.games` - show available mini-games
     \n`.write_top <number_of_rows>` - create message for subscription
     \n`.set_message_id <id>` - set id of subscription message
     \n`.add_role <emojii> <jam_num_in_top> <role_id>` - adds emojii that acts like a button for subscription''',
                          colour=0x87CEEB)
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
        asyncio.create_task(timer("test", "sadasda", ctx, 30)))


@bot.command()
async def write_top(ctx, num: int):
    global list_len
    num = min(10, num)
    message = await ctx.send('\n'.join([f"{i + 1} - " for i in range(num)]))
    list_len = num
    global role_message_id
    role_message_id = message.id
    await asyncio.gather(
        asyncio.create_task(timer("test", "sadasda", ctx, 30)))


@bot.command()
async def add_role(ctx, emoji, jam_num: int, role_id: int):
    emoji_to_role[discord.PartialEmoji(name=emoji)] = role_id
    roles_dct[discord.PartialEmoji(name=emoji)] = get(ctx.guild.roles, id=role_id)
    roles_dct_num[jam_num] = role_id
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
bot.run('')
