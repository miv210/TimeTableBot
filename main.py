from library import config
import telebot
from telebot import types
from datetime import datetime, timedelta
from library.parser import parser
from library.bd import read_bd


dir_file = input('Введите полный пкть, где буду хранится doc файлы, вводить нужно с обратными слешами "/" или двойными "\": ')
print(dir_file)
#Проверка на спам
def spam(text):
    global last_time

    start_pars = parser()

    time = datetime.now() - last_time

    if time.seconds >= 300:
        last_time = datetime.now()
        start_pars.start(dir_file)

    time_table = read_bd(text)
    return time_table

#Словарь введеной группы
globalChat = {}
last_time = datetime.now() - timedelta(minutes=30)
def global_chat_start(user_id, group='Не указана группа', sleep=0):
    if not user_id in globalChat:
        chat = {'sleep': sleep, 'group': group}
        globalChat[user_id] = chat

#Подключение к телеграмм API
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    global_chat_start(user_id)

    text_start(message)


def text_start(message):
    main = bot.send_message(message.chat.id, '''Чтобы узнать расписание введите название группы в формате "301прг" ''',
                            reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(main, save_group)


def save_group(message):
    user_id = message.from_user.id
    globalChat[user_id]['group'] = message.text
    save_or_change(message)


def save_or_change(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton('Да')
    change = types.KeyboardButton('Изменить имя группы')
    markup.add(yes, change)
    main = bot.send_message(message.chat.id, f'Ваша группа {globalChat[user_id]["group"]}?', reply_markup=markup)
    bot.register_next_step_handler(main, check)


def check(message):
    if message.text == 'Да':
        parser_1(message)
    elif message.text == 'Изменить имя группы':
        user_id = message.from_user.id
        globalChat[user_id]['group'] = 'Не указана группа'
        text_start(message)
    elif message.text == 'Получить расписание':
        send_timetable(message)
    else:
        main = bot.send_message(message.chat.id, 'Используйте кнопки, для управления ботом')
        bot.register_next_step_handler(main, check)


def parser_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_button = types.KeyboardButton('Получить расписание')
    change_group = types.KeyboardButton('Изменить имя группы')
    markup.add(save_button, change_group)
    main = bot.send_message(message.chat.id, 'Сохранено', reply_markup=markup)
    bot.register_next_step_handler(main, check)


def send_timetable(message):
    user_id = message.from_user.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_button = types.KeyboardButton('Получить расписание')
    change_group = types.KeyboardButton('Изменить имя группы')
    markup.add(save_button, change_group)

    bot.send_message(message.chat.id, 'Идет проверка, ожидайте...', reply_markup=types.ReplyKeyboardRemove())
    time_table = spam(globalChat[user_id]['group'])
    main = bot.send_message(message.chat.id, time_table, reply_markup=markup)

    print(globalChat)
    bot.register_next_step_handler(main, check)



bot.polling(none_stop=True)