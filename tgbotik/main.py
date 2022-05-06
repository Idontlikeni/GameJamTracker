import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import datetime as dt
import sqlite3
import random
import datetime
import asyncio

bot = telebot.TeleBot('5163172103:AAHmUeEMMw_NrG8TiY-ZZbasxjs806DAVRc')
# 704213045


names = []
dates = []
links = []
htm = ''
images = []
cou = 0
phs = []
idsph = []
flood = []
id_otvet = 0
id_pay = 0
admins = []
desk = []
vips = []

markup = types.ReplyKeyboardMarkup()
itembtnhelp = types.KeyboardButton('/help')
itembtna = types.KeyboardButton('/id')
itembtno = types.KeyboardButton('/about us')
markup.add(itembtnhelp, itembtna, itembtno)

markup_c = types.ReplyKeyboardMarkup()
itembtnyes = types.KeyboardButton('yes')
itembtnno = types.KeyboardButton('no')
markup_c.add(itembtnyes, itembtnno)

conf = types.ReplyKeyboardMarkup()
itembtnyesc = types.KeyboardButton('yes')
itembtnnoc = types.KeyboardButton('no')
conf.add(itembtnyesc, itembtnnoc)

con = sqlite3.connect("tg_bot", check_same_thread=False)
cur = con.cursor()

result = cur.execute("""SELECT t.id_vip_1 FROM data_telega AS t""").fetchall()
for item in result:
    vips.append(item[0])
result = cur.execute("""SELECT id_admin FROM admins""").fetchall()
for item in result:
    admins.append(item[0])

ids = cur.execute(f"""SELECT id FROM desk""").fetchall()
con.close()
print(ids, admins, vips)

# -------------------------------------------------------------------------------------
url = 'https://itch.io/jams'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
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


def parser(url):

    games = []
    imgs = []
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name1 = soup.find_all('div', class_="stat_header_widget")
    soup1 = BeautifulSoup(str(name1[0]), 'html.parser')
    name = str(soup1.find_all('h2')[0])
    name = name.split('>')[1].split('<')[0]
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
    htm = f'Информация отсутствует по {name}'
    if len(games) != 0:
        htm = ''
        htm += f'Profile: {name}\n'
        for i in range(len(games)):
            htm += f'=========================\n {games[i]}\n {links[i]}\n'
    return htm


# --------------------------------------------------------------------------------------

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global phs, cou, id_otvet, idsph, id_pay, desk, ids
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Вас приветствует телеграм бот Game Jams Bot."
                                               " Напишите /help для продолжения", reply_markup=markup)


    elif message.text == "/gst":
        for i in range(len(names)):
            bot.send_message(message.from_user.id, f'{names[i]}\n{dates[i]}\nhttps://itch.io{links[i]}')


    elif message.text == "/help":
        if message.from_user.id in admins:
            bot.send_message(message.from_user.id, "/gst - выводит даты начала ближайших game jams \n"
                                                   "/id - выводит id пользователя \n"
                                                   "/file - отправляет фото \n"
                                                   "/about us - информация о разработчиках\n"
                                                   "/support - отправить сообщение разработичку\n"
                                                   "/payment - оплатить вип доступ\n"
                                                   "/answer [id] - ответить пользователю по айди\n"
                                                   "/desk - посмотреть доску обьявление поиска команды\n"
                                                   "/create_desk - создать свое обьявление по поиску команды\n"
                                                   "/timer [ч] [м] [с] - установить таймер(вип функция)\n"
                                                   "------админское------\n"
                                                   "/clear - очищает бесполезный список фото\n"
                                                   "/check - выводит список фото АБСОЛЮТНО ЮЗЛЕСС\n"
                                                   "/confirm [id] - подтверждение оплаты\n"
                                                   "/reject [id] - добавить пользователя в список флуда, "
                                                   "следующее сообщение [yes/no]\n"
                                                   "/bd - выводит базу данных\n"
                                                   "/cl_bd [id] - чистит определенную позицию в бд\n"
                                                   "/flood_del [id] - убирает пользователя из флуд списка\n"
                                                   "/cl_desk [i] - убирает обьявление")
        else:
            bot.send_message(message.from_user.id, "/gst - выводит даты начала ближайших game jams \n"
                                                   "/id - выводит id пользователя \n"
                                                   "/file - отправляет фото \n"
                                                   "/about us - информация о разработчиках\n"
                                                   "/support - отправить сообщение разработичку\n"
                                                   "/payment - оплатить вип доступ\n"
                                                   "/answer [id] - ответить пользователю по айди\n"
                                                   "/desk - посмотреть доску обьявление поиска команды\n"
                                                   "/create_desk - создать свое обьявление по поиску команды\n"
                                                   "/timer [ч] [м] [с] - установить таймер(вип функция)\n")



    elif message.text == "/id":
        bot.send_message(message.from_user.id, message.chat.id)


    elif message.text == "/file":
        photo = open('res.jpg', 'rb')
        bot.send_photo(message.from_user.id, photo)
        photo.close()


    elif message.text == "/about us":
        photo = open('res.jpg', 'rb')
        bot.send_photo(message.from_user.id, photo, "Мы команда учеников яндекс лицея и это телеграм бот нашего"
                                                    " проекта. Здесь вы можете узнать его возможносях и ими "
                                                    "воспользоваться.")
        photo.close()


    elif message.text == "/support":
        bot.send_message(message.from_user.id, "Напишите ваше сообщение для разработчика")
        bot.register_next_step_handler(message, ans)


    elif message.text == "/payment":
        text = "Получение ВИП доступа дает вам" \
               " приоритетный показ в доске обьявлений"
        bot.send_message(message.from_user.id, text)
        if message.from_user.id not in flood:
            daten = dt.datetime.now()
            daten = str(daten)
            code = random.randint(10000, 99999)
            bot.send_message(message.from_user.id, "отправьте фото с платежом {}".format(code))

            @bot.message_handler(content_types=["photo"])
            def photo(message):
                idphoto = message.photo[0].file_id
                bot.send_message(704213045, "кто-то произвел оплату, всего непрочитанных: {}".format(cou))
                bot.send_message(message.from_user.id, "фото отправленно")
                idsph.append("{}, {}, {}".format(code, daten, message.from_user.id))
                phs.append(idphoto)
                print(idphoto)
                sqlite_connection = sqlite3.connect('tg_bot')
                cursor = sqlite_connection.cursor()
                sqlite_insert_with_param = """INSERT INTO dateofpays
                                      (tg_id, date, code, photo_id)
                                      VALUES (?, ?, ?, ?);"""
                data_tuple = (message.from_user.id, str(daten), code, idphoto)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqlite_connection.commit()
                cursor.close()

            cou += 1
        else:
            bot.send_message(message.from_user.id, "Вы были замечены во флуде и больше не имеете возможности"
                                                   " отправлять фотографии, если остались вопросы, то пишите "
                                                   "(/support)")

    elif message.text == "/check":
        if message.from_user.id in admins:
            if phs:
                for i in range(len(phs)):
                    bot.send_photo(704213045, phs[i], idsph[i], reply_markup=markup_c)
            else:
                bot.send_message(704213045, "новых фотографий не было")
        else:
            bot.send_message(message.from_user.id, "отказано в доступе")



    elif message.text == "/clear":
        if message.from_user.id in admins:
            phs = []
            bot.send_message(704213045, "готово")
        else:
            bot.send_message(message.from_user.id, "отказано в доступе")



    elif message.text.split()[0] == "/answer":
        try:
            m = message.text.split()
            id_otvet = m[1]
            bot.send_message(message.from_user.id, "введите сообщение")
            bot.register_next_step_handler(message, otvet)
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")

    elif message.text == "/test":
        pass

    elif message.text.split()[0] == "/confirm":
        try:
            m = message.text.split()
            id_pay = m[1]
            if message.from_user.id in admins:
                sqlite_connection = sqlite3.connect('tg_bot')
                cursor = sqlite_connection.cursor()
                cursor.execute("""INSERT INTO data_telega (id_vip_1) VALUES ({})""".format(id_pay))
                sqlite_connection.commit()
                cursor.close()
                bot.send_message(704213045, "confd {}".format(id_pay))
                bot.send_message(id_pay, "ваша оплата подтверждена")
            else:
                bot.send_message(message.from_user.id, "отказано в доступе")
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")


    elif message.text.split()[0] == "/reject":
        try:
            m = message.text.split()
            id_pay = m[1]
            if message.from_user.id in admins:
                bot.send_message(704213045, "подтверждаем {}? [yes/no]".format(id_pay))
                bot.send_message(id_pay, "платеж не подтвержден, отправьте сообщение "
                                         "с кодом указанном при оплате (/support)")
                bot.register_next_step_handler(message, confirm)
            else:
                bot.send_message(message.from_user.id, "отказано в доступе")
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")


    elif message.text == "/bd":
        if message.from_user.id in admins:
            sqlite_connection = sqlite3.connect('tg_bot')
            cursor = sqlite_connection.cursor()
            result = cursor.execute("""
            SELECT * FROM dateofpays
            """).fetchall()
            cursor.close()
            for item in result:
                stroka = str(str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]))
                bot.send_photo(704213045, item[4], stroka)
        else:
            bot.send_message(message.from_user.id, "отказано в доступе")


    elif message.text.split()[0] == "/cl_bd":
        try:
            if message.from_user.id in admins:
                sqlite_connection = sqlite3.connect('tg_bot')
                cursor = sqlite_connection.cursor()
                result = cursor.execute(f"""
                            DELETE FROM dateofpays WHERE id = {message.text.split()[1]}
                            """).fetchall()
                sqlite_connection.commit()
                cursor.close()
            else:
                bot.send_message(message.from_user.id, "отказано в доступе")
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")

    elif message.text.split()[0] == "/flood_del":
        try:
            if message.from_user.id in admins:
                sqlite_connection = sqlite3.connect('tg_bot')
                cursor = sqlite_connection.cursor()
                result = cursor.execute(f"""
                            DELETE FROM floodban WHERE id_flood = {message.text.split()[1]}
                            """).fetchall()
                flood.remove(message.text.split()[1])
                bot.send_message(704213045, "успешно")
                print(flood)
                sqlite_connection.commit()
                cursor.close()
            else:
                bot.send_message(message.from_user.id, "отказано в доступе")
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")
        except ValueError:
            bot.send_message(70421045, "айди не в списке")

    elif message.text == "/desk":
        if ids:
            con = sqlite3.connect("tg_bot", check_same_thread=False)
            cur = con.cursor()
            try:
                if message.from_user.id not in flood:
                    for i in range(len(ids)):
                        author = cur.execute(f"""SELECT author FROM desk WHERE id = {ids[i][0]}""").fetchall()[0][0]
                        profile = cur.execute(f"""SELECT profile FROM desk WHERE id = {ids[i][0]}""").fetchall()[0][0]
                        text = cur.execute(f"""SELECT text FROM desk WHERE id = {ids[i][0]}""").fetchall()[0][0]
                        id_d = cur.execute(f"""SELECT id FROM desk WHERE id = {ids[i][0]}""").fetchall()[0][0]
                        vip = cur.execute(f"""SELECT vip FROM desk WHERE id = {ids[i][0]}""").fetchall()[0][0]
                        temp_desk = f'{id_d} автор: {author}, ' \
                                    f'профиль: {profile}, ' \
                                    f'текст: {text}'
                        print((id_d, vip, f'{id_d} автор: {author}', f'профиль: {profile}', f'текст: {text}'))
                        temp_desk = (str(id_d), str(vip), f'автор: {author}', f'профиль: {profile}', f'текст: {text}')
                        bot.send_message(message.from_user.id, " ".join(temp_desk))
                else:
                    bot.send_message(message.from_user.id, "Вы находитесь в черном списке, отпишите разработчику,"
                                                           " если это было сделано по ошибке")
            except IndexError:
                print("ошибочка")
            con.close()
        else:
            bot.send_message(message.from_user.id, "Доска обьявлений сейчас пустует")

    elif message.text == "/create_desk":
        bot.send_message(message.from_user.id, "напишите обьявление в формате:\n"
                                               "[ваше имя (без пробелов] [имя вашего профиля] [текст вашего обьявления"
                                               " например ваши контакты и кого вы ищите]")
        bot.register_next_step_handler(message, crd)

    elif message.text.split()[0] == "/profile":
        try:
            bot.send_message(message.from_user.id, parser(f'https://itch.io/profile/{message.text.split()[1]}'))
        except IndexError:
            bot.send_message(message.from_user.id, "Такого профиля не существует")

    elif message.text.split()[0] == "/cl_desk":
        try:
            if message.from_user.id in admins:
                sqlite_connection = sqlite3.connect('tg_bot')
                cursor = sqlite_connection.cursor()
                result = cursor.execute(f"""
                            DELETE FROM desk WHERE id = {message.text.split()[1]}
                            """).fetchall()
                bot.send_message(704213045, "успешно")
                sqlite_connection.commit()
                cursor.close()
            else:
                bot.send_message(message.from_user.id, "отказано в доступе")
        except IndexError:
            bot.send_message(message.from_user.id, "неверный айди")
        except ValueError:
            bot.send_message(70421045, "айди не в списке")
        con = sqlite3.connect("tg_bot", check_same_thread=False)
        cur = con.cursor()
        ids = cur.execute(f"""SELECT id FROM desk""").fetchall()
        con.close()

    elif message.text.split()[0] == "/timer":
        if message.from_user.id in vips:
            m = message.text.split()
            try:
                hs = int(m[1])
                mins = int(m[2])
                secds = int(m[3])
                print(hs, mins, secds)
                now = datetime.datetime.now()
                if now.hour + hs > 24:
                    bot.send_message(message.from_user.id, "Часы не должны уходить на другой день")
                if now.second + secds > 60:
                    bot.send_message(message.from_user.id, "Секунды не должны уходить на следующую минуту")
                if now.hour + mins > 60:
                    bot.send_message(message.from_user.id, "Минуты не должны уходить на другой час")
                bot.send_message(message.from_user.id, f'засек {message.text[1:]}')
                while datetime.datetime.now().minute != now.minute + mins and\
                        datetime.datetime.now().second != now.second + secds and\
                        datetime.datetime.now().hour != now.hour + hs:
                    pass
                bot.send_message(message.from_user.id, "end")
            except IndexError:
                bot.send_message(message.from_user.id, "Недостаточно аргументов")
            except ValueError:
                bot.send_message(message.from_user.id, "Неверное значение ")
        else:
            bot.send_message(message.from_user.id, "Отказано в доступе")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def ans(message):
    bot.send_message(704213045, "сообщение от пользователя: \"{}\". Его айди - {}".format(message.text,
                                                                                          message.from_user.id))
    bot.send_message(message.from_user.id, "сообщение отправлено")

    # добавить функцию получении новых фоторафий и отправление уведолмения при получении


def otvet(message):
    global id_otvet
    bot.send_message(int(id_otvet), "вам пришло сообщение от {}".format(message.from_user.id))
    bot.send_message(message.from_user.id, "сообщение отправлено {}".format(id_otvet))
    bot.send_message(int(id_otvet), message.text)


def confirm(message):
    if message.text == "yes":
        bot.send_message(id_pay, "вы были отправлены в список нарушителей за неверное фото,"
                                 "если это было сделано по ошибке напишите в поддержку "
                                 "(/support)")
        sqlite_connection = sqlite3.connect('tg_bot')
        cursor = sqlite_connection.cursor()
        cursor.execute("""INSERT INTO floodban (id_flood) VALUES ({})""".format(id_pay))
        sqlite_connection.commit()
        cursor.close()
    elif message.text == "no":
        pass

def crd(message):
    global ids, conf
    v = False
    m = message.text.split()
    if len(m) >= 3:
        bot.send_message(message.from_user.id, f'проверьте ваше обьявление: \n'
                                           f'автор: {m[0]}, профиль: {m[1]}, текст: {" ".join(m[2:])}', reply_markup=conf)
        sqlite_connection = sqlite3.connect('tg_bot')
        cursor = sqlite_connection.cursor()
        try:
            if message.from_user.id in vips:
                v = True
            sqlite_insert_with_param = """INSERT INTO desk
                                                              (author, profile, text, vip)
                                                              VALUES (?, ?, ?, ?);"""
            data_tuple = (m[0], m[1], " ".join(m[2:]), v)
            print(data_tuple)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            bot.send_message(message.from_user.id, "Вашу неверную запись удалят в скором времени")
        except IndexError:
            bot.send_message(message.from_user.id, "ошибка")

        ids = cursor.execute(f"""SELECT id FROM desk""").fetchall()
        cursor.close()
        bot.register_next_step_handler(message, crd)
    else:
        if message.text == "yes":
            bot.send_message(message.from_user.id, "Отправлено на доску")
        elif message.text == "no":
            con = sqlite3.connect("tg_bot", check_same_thread=False)
            cur = con.cursor()
            ids = cur.execute(f"""SELECT id FROM desk""").fetchall()
            con.close()
            bot.send_message(704213045, f"удалить запись с айди {ids[-1][0]}")
            bot.send_message(message.from_user.id, "Напишите ваше сообщение еще раз")
            bot.register_next_step_handler(message, crd)
        else:
            bot.send_message(message.from_user.id, "Неверное обьявление")

bot.polling(none_stop=True, interval=0)

# sqlite_connection = sqlite3.connect('tg_bot')
# cursor = sqlite_connection.cursor()
# result = cursor.execute("""
#             SELECT * FROM dateofpays
#             """).fetchall()
# sqlite_connection.commit()
# cursor.close()


# if message.from_user.id in admins:
#
# else:
#     bot.send_message(message.from_user.id, "отказано в доступе")

# try:
#
# except IndexError:
#     bot.send_message(message.from_user.id, "неверный айди")


# автор: {здесь селект из бд}
# профиль: {ссылка на профиль автора}
# текст: {текст обьявления}

# con = sqlite3.connect("tg_bot", check_same_thread=False)
# cur = con.cursor()
# ids = cur.execute(f"""SELECT id FROM desk""").fetchall()
# con.close()
