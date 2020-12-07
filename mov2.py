from telebot import types
import urllib3
import telebot
from urllib.request import urlopen
import json
import urllib.parse
from telegram import Update
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import MessageHandler
import os
from flask import Flask, request
import mysql.connector
import threading
import urllib.request


bot = telebot.TeleBot("1435788509:AAF7Yflxr6VBWs-tAecxNPXkGfiIbZ4Y2JQ")
TOKEN = '1435788509:AAF7Yflxr6VBWs-tAecxNPXkGfiIbZ4Y2JQ'

eror = '🤷‍♂️*Результатов не найдено. Возможно фильма или сериала с таким названием нет или вы ввели название с ошибкой.*' \
       '\n' \
       '\n' \
       'Попробуйте еще раз! Отправьте мне название фильма или сериала как оно пишется в Кинопоиске. *Год фильма или сериала, какой сезон и какая серия при поиске писать не нужно!!*' \
       "\n" \
       "\n" \

podptext = 'Привет друзья! Наш бот абсолютно бесплатен и без рекламы! Но доступ у него открыт только подписчикам нашего канала👉 ' + '[Фильмы и Сериалы Онлайн]' + '(https://t.me/filmyuserialy)' \
                                                                                                                                                            "\n" \
                                                                                                                                                            "\n" \
                                                                                                                                                            'Подпишитесь, что бы не пропускать новинки! *После подписки нажмите кнопку "Я подписался". Доступ будет открыт автоматически.*'

privet = "👋Добро пожаловать в поиск! Напиши мне название фильма, мультфильма или сериала и я найду их для тебя." \
         "\n" \
         "\n" \
         '❗️*ВАЖНО!* Год выпуска, номер сезона или номер серии *писать не нужно!* Название должно быть правильным (как в Кинопоиске)! В обратном случае, я ничего не смогу найти для тебя. Например:' \
         "\n" \
         "\n" \
         "*✅Правильно:*  Ведьмак" \
         "\n" \
         "*✅Правильно:* The Witcher" \
         "\n" \
         '*❌Неправильно:* Ведьмак 2019' \
         "\n" \
         '*❌Неправильно:* Ведьмак 1 сезон' \
         "\n" \
         "\n" \
         'Жду от тебя названия фильма👇' \
         "\n" \
         'Приятного просмотра!🍿'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global podptext
    global privet

    fname = str(message.from_user.first_name)
    lname = str(message.from_user.last_name)
    userN = str(message.from_user.username)
    userId = int(message.from_user.id)
    try:
        mydb = mysql.connector.connect(host="searchbottgdb.cgz9qiqrxgau.eu-central-1.rds.amazonaws.com", user='searchbottgdb', passwd='searchbottgdb_password', database='searchbottgdb')
        mycursor = mydb.cursor()
        sqlform = 'Insert into Members2(usernames, userid, imya, famil) values(%s, %s, %s, %s)'
        Userss = [(userN, userId, fname, lname)]
        mycursor.executemany(sqlform, Userss)
        mydb.commit()
        mydb.close()        
        chri = "member" 
        try:
            status = bot.get_chat_member(-1001348830793, user_id=message.from_user.id).status
        except telebot.apihelper.ApiException:
            status = False
        if chri == status:
            bot.send_message(message.chat.id, privet, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        else:
            urlpod = "https://t.me/filmyuserialy"
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Подписаться ➡️', url=urlpod)
            url_button2 = types.InlineKeyboardButton(text="Я подписался 👍", callback_data='testp')
            keyboard.add(url_button)
            keyboard.add(url_button2)
            bot.send_message(message.chat.id, podptext, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
                             reply_markup=keyboard)
    except mysql.connector.Error:
        bot.send_message(message.chat.id, 'Попробуйте снова. Нажмите /start', parse_mode=ParseMode.MARKDOWN)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global privet
    global podptext
    if call.message:
        if call.data == 'testp':
            chri = "member" 
            try:
                status = bot.get_chat_member(-1001348830793, user_id=call.from_user.id).status
            except telebot.apihelper.ApiException:
                status = False
            if chri == status:
                bot.send_message(call.message.chat.id, privet, parse_mode=ParseMode.MARKDOWN,
                                 disable_web_page_preview=True)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Вы не подписаны на канал!🤷‍♂️ Подпишитесь!")


@bot.message_handler(content_types=['text'])
def bad_poisk(message):
    global eror
    global podptext
    chri = "member"   
    try:
        try:
            status = bot.get_chat_member(-1001348830793,
                                         user_id=message.from_user.id).status
        except telebot.apihelper.ApiException:
            status = False
        if chri == status:
            if len(message.text) > 3:
                try:
                    x = int(message.text) + 1
                    bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN,
                                     disable_web_page_preview=True)
                except ValueError:
                    userN = str(message.from_user.username)
                    userId = int(message.from_user.id)

                    fname = str(message.from_user.first_name)
                    lname = str(message.from_user.last_name)

                    z = 'http://playeronline.pro/api/videos.json?title=' + urllib.parse.quote(
                        message.text) + '&token=0b4c43c4ffed666cefe78e9bc99447ed'
                    try:

                        with urlopen(z) as response:

                            source = response.read()
                        try:

                            data = json.loads(source)

                            if len(data) <= 0:
                                bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN,
                                                 disable_web_page_preview=True)
                            else:
                                for i in data:
                                    if i['type'] == 'movie':
                                        url1 = 'http://playeronline.pro/movie/' + i['token'] + '/iframe?d=hd.kinolive.su'
                                        otvet = '[' + '🎥' + ']' + '(' + i['poster'] + ')' + '*' + i[
                                            'title_ru'] + " " + '(' + str(i['year']) + '/' + i[
                                                    'quality'] + ')' + '*' + '\n' \
                                                + 'Озвучка:' + " " + i['translator'] + '\n' + '\n' \
                                                + '[👁‍🗨СМОТРЕТЬ ФИЛЬМ]' + '(' + url1 + ')' \
                                                                                         "\n" \
                                                                                         "\n" \
                                                                                         '[🔍ПОИСК ФИЛЬМОВ]' + '(http://t.me/kinolivesu_bot)' \

                                        url2 = "https://t.me/kinolivesu_bot"
                                        url3 = "https://t.me/filmyuserialy"
                                        keyboard = types.InlineKeyboardMarkup()
                                        url_button = types.InlineKeyboardButton(text="Смотреть фильм", url=url1)
                                        url_button2 = types.InlineKeyboardButton(text="🔍Поиск фильмов", url=url2)
                                        url_button3 = types.InlineKeyboardButton(text="🔥Лучшие Фильмы🔥", url=url3)
                                        keyboard.add(url_button)
                                        keyboard.add(url_button2)
                                        keyboard.add(url_button3)
                                        bot.send_message(message.chat.id, otvet, parse_mode=ParseMode.MARKDOWN,
                                                         disable_web_page_preview=False, reply_markup=keyboard)



                                    elif i['type'] == 'serial':
                                        url1 = 'http://playeronline.pro/serial/' + i['token'] + '/iframe?d=hd.kinolive.su'
                                        otvet = '[' + '🎥' + ']' + '(' + i['poster'] + ')' + '*' + i[
                                            'title_ru'] + " " + '(' + str(i['year']) + '/' + i[
                                                    'quality'] + ')' + '*' + '\n' \
                                                + 'Озвучка:' + " " + i['translator'] + '\n' + '\n' \
                                                + '[👁‍🗨СМОТРЕТЬ СЕРИАЛ]' + '(' + url1 + ')' \
                                                                                          "\n" \
                                                                                          "\n" \
                                                                                          '[🔍ПОИСК ФИЛЬМОВ]' + '(http://t.me/kinolivesu_bot)' \

                                        url2 = "https://t.me/kinolivesu_bot"
                                        url3 = "https://t.me/filmyuserialy"
                                        keyboard = types.InlineKeyboardMarkup()
                                        url_button = types.InlineKeyboardButton(text="Смотреть сериал", url=url1)
                                        url_button2 = types.InlineKeyboardButton(text="🔍Поиск фильмов", url=url2)
                                        url_button3 = types.InlineKeyboardButton(text="🔥Лучшие Фильмы🔥", url=url3)
                                        keyboard.add(url_button)
                                        keyboard.add(url_button2)
                                        keyboard.add(url_button3)
                                        bot.send_message(message.chat.id, otvet, parse_mode=ParseMode.MARKDOWN,
                                                         disable_web_page_preview=False, reply_markup=keyboard)
                        except json.decoder.JSONDecodeError:
                            bot.send_message(message.chat.id,
                                             "Извините, у нас технические работы на сервере. Мы скоро закончим:) Пожалуйста, вернитесь позже.",
                                             parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                    except urllib.error.URLError:
                        bot.send_message(message.chat.id,
                                         "Сейчас в работе телеграм BotApi наблюдаются сбои, поэтому на ваш запрос не поступило ответа от сервера. Вы можете попробовать еще раз или вернуться позже. Приносим вам свои извинения за неудобства!",
                                         parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        else:
            urlpod = "https://t.me/filmyuserialy"
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Подписаться ➡️', url=urlpod)
            url_button2 = types.InlineKeyboardButton(text="Я подписался 👍", callback_data='testp')
            keyboard.add(url_button)
            keyboard.add(url_button2)
            bot.send_message(message.chat.id, podptext, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
                             reply_markup=keyboard)
    except Exception:
        bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


tr1 = threading.Thread(target=send_welcome).start()
tr2 = threading.Thread(target=callback_inline).start()
tr3 = threading.Thread(target=bad_poisk).start()

# bot.polling(none_stop=True)

server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    TOKEN = '1435788509:AAF7Yflxr6VBWs-tAecxNPXkGfiIbZ4Y2JQ'
    bot.remove_webhook()
    bot.set_webhook(url='https://searchbottg.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))
