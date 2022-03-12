import telebot
from telebot import types
from gst import names, dates, links

bot = telebot.TeleBot('5163172103:AAHmUeEMMw_NrG8TiY-ZZbasxjs806DAVRc')
markup = types.ReplyKeyboardMarkup()
itembtngst = types.KeyboardButton('/gst')
itembtnhelp = types.KeyboardButton('/help')
markup.row(itembtngst, itembtnhelp)
bot.send_message(704213045, "Выберете действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/gst":
        for i in range(len(names)):
            bot.send_message(message.from_user.id, f'{names[i]}\n{dates[i]}\nhttps://itch.io{links[i]}')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/gst - выводит даты начала ближайших game jams")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
