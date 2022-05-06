import discord
import logging
import requests
import datetime as dt
from bs4 import BeautifulSoup
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "OTM2OTE2Mzk3NzA2MDY3OTcw.YfUJZA.5x_By5eHYxwYWJnIdMhzcBcAdqo"
select = False
names = []
dates = []
links = []
images = []


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def timer(self, name, date, message, jam_time):
        await message.channel.send(f'Таймер на {name} {date} успешно установлен.')
        while True:
            if jam_time < dt.datetime.now():
                await message.channel.send('⏰ Time has come')
                break
            await asyncio.sleep(300)

    async def on_message(self, message):
        global select, names, dates, links, images
        if message.author == self.user:
            return 
        if select:
            try:
                num = int(message.content.lower()) - 1
                name = names[num]
                date = dates[num]
                date, time = date.split()
                year, month, day = list(map(int, date.split('-')))
                hour, minute, second = list(map(int, time.split(':')))
                # delta_time1 = dt.timedelta(days=5, hours=2, minutes=25)
                jam_time = dt.datetime(year, month, day, hour, minute, second)
                # print(jam_time)
                select = False
                await asyncio.gather(asyncio.create_task(client.timer(name, date, message, jam_time)))
            except:
                await message.channel.send('Напишите проядковый номер желаемого для отслеживания джема.')
                select = True
        elif "set_timer" in message.content.lower():
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
                await message.channel.send(f'{names[i]}\n{dates[i]}\nhttps://itch.io{links[i]}')
                await message.channel.send(f'☝{i + 1}-й')
            await message.channel.send('Выберите желательный для отслеживания джем.')
            select = True
        elif "test" in message.content.lower():
            await message.channel.send('Тест успешно пройден!')


intents = discord.Intents.default()
intents.members = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
logger.setLevel(logging.INFO)