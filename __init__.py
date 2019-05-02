import sqlite3
from telebot import types
import telebot
bot = telebot.TeleBot('828307998:AAHGY_swAB45QvwNrD3sJ_2Cl8O0JQfRUXY')


day = 0
month = 0
year = 0
goals_num = 0
cur_goals_num = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()
        key_create = types.InlineKeyboardButton(text='Добавить список дел', callback_data='create')
        keyboard.add(key_create)
        key_show = types.InlineKeyboardButton(text='Показать текущий список дел', callback_data='show')
        keyboard.add(key_show)
        question = 'Выберите действие:'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Напишите /start')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'create':
        bot.send_message(call.message.chat.id, 'Отлично, давайте выберем дату!')
        bot.send_message(call.message.chat.id, 'Введите год')
        bot.register_next_step_handler(call.message, get_year)
    elif call.data == 'show':
        with sqlite3.connect('example.db') as conn:
            cur = conn.cursor()
            global day
            global month
            global year
            f = open('save.txt', 'r')
            day = int(f.readline())
            month = int(f.readline())
            year = int(f.readline())
            f.close()
            query = ('''SELECT plans.num, plans.goal
                   FROM plans''')
            cur.execute(query)
            rows = cur.fetchall()
            bot.send_message(call.message.chat.id,
                             'Предыдущие планы')
            bot.send_message(call.message.chat.id, 'Планы на {DAY}.{MONTH}.{YEAR}'.format(DAY=day, MONTH=month, YEAR=year))
            for row in rows:
                num, goal = row
                result = str(num) + '. ' + str(goal)
                bot.send_message(call.message.chat.id, result)


def get_year(message):
    global year
    if int(message.text) >= 2019:
        year = message.text
        bot.send_message(message.chat.id, 'Выберите месяц')
        bot.register_next_step_handler(message, get_month)
    else:
        bot.send_message(message.from_user.id, 'Введите корректный год')
        bot.register_next_step_handler(message, get_year)


def get_month(message):
    global month
    if int(message.text) > 12 or int(message.text) < 1:
        bot.send_message(message.from_user.id, 'Введите корректный месяц')
        bot.register_next_step_handler(message, get_month)
    else:
        month = message.text
        bot.send_message(message.from_user.id, 'Выберите день')
        bot.register_next_step_handler(message, get_day)


def get_day(message):
    global day
    global month
    global year
    global goals_num
    if int(message.text) < 1 or int(message.text) > 31:
        bot.send_message(message.from_user.id, 'Введите корректный день')
        bot.register_next_step_handler(message, get_day)
    elif month == 2:
        if (year % 100 == 0 or year % 4 == 0) and year % 400 != 0:
            if int(message.text) > 29:
                bot.send_message(message.from_user.id, 'Введите корректный день')
                bot.register_next_step_handler(message, get_day)
            else:
                day = message.text
                bot.send_message(message.from_user.id, 'Введите количество целей на день')
                bot.register_next_step_handler(message, get_goals_num)
        elif int(message.text) > 28:
            bot.send_message(message.from_user.id, 'Введите корректный день')
            bot.register_next_step_handler(message, get_day)
        else:
            day = message.text
            bot.send_message(message.from_user.id, 'Введите количество целей на день')
            bot.register_next_step_handler(message, get_goals_num)
    elif month == 4 or month == 6 or month == 9 or month == 11:
        if int(message.text) > 30:
            bot.send_message(message.from_user.id, 'Введите корректный день')
            bot.register_next_step_handler(message, get_day)
        else:
            day = message.text
            bot.send_message(message.from_user.id, 'Введите количество целей на день')
            bot.register_next_step_handler(message, get_goals_num)
    else:
        day = message.text
        bot.send_message(message.from_user.id, 'Введите количество целей на день')
        bot.register_next_step_handler(message, get_goals_num)


def get_goals_num(message):
    global goals_num
    goals_num = int(message.text)
    with sqlite3.connect('example.db') as conn:
        cur = conn.cursor()
        create_tables(cur, conn)
        bot.send_message(message.from_user.id, 'Введите свои планы на день: {plan}'.format(plan=goals_num))
        bot.register_next_step_handler(message, cin_goals)


def select_all_goals(message):
    global day
    global month
    global year
    f = open('save.txt', 'w')
    f.write(day + '\n')
    f.write(month + '\n')
    f.write(year + '\n')
    f.close()
    with sqlite3.connect('example.db') as conn:
        cur = conn.cursor()
        query = '''SELECT plans.num, plans.goal
                   FROM plans'''
        cur.execute(query)
        rows = cur.fetchall()
        bot.send_message(message.from_user.id, 'Планы на {DAY}.{MONTH}.{YEAR}'.format(DAY=day, MONTH=month, YEAR=year))
        for row in rows:
            num, goal = row
            result = str(num) + '. ' + str(goal)
            bot.send_message(message.from_user.id, result)


def create_tables(cur, conn):
    cur.execute('DROP TABLE IF EXISTS plans')
    cur.execute('''
        CREATE TABLE plans (
            num INTEGER PRIMARY KEY AUTOINCREMENT,
            goal VARCHAR(255)
        )''')
    conn.commit()


def cin_goals(message):
    with sqlite3.connect('example.db') as conn:
        cur = conn.cursor()
        global cur_goals_num
        global goals_num
        cur_goal = str(message.text)
        cur.execute('''
                   INSERT INTO plans (goal) VALUES 
                       (?)''', [cur_goal])
        bot.send_message(message.from_user.id, 'Принято')
        conn.commit()
        cur_goals_num += 1
        if cur_goals_num == goals_num:
            select_all_goals(message)
        else:
            bot.register_next_step_handler(message, cin_goals)


bot.polling(none_stop=True, interval=0)
