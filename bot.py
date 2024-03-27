import telebot
from telebot import types

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")

import numpy as np
from numpy import sin, cos, tan, arccos, arcsin, arctan


token = '6997575305:AAF--tYpGyBzwgNXvTRDOUkhYsi8E5HU-f4'
bot = telebot.TeleBot(token)


#start and restart bot
@bot.message_handler(commands=["start", "restart"])
def start(message):
    #greeting
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}, я бот по построению графиков функций!")
    cat = open("cute_cat.jpeg", "rb")
    bot.send_photo(message.chat.id, cat)

    #answer yes to start using
    markup = types.InlineKeyboardMarkup(row_width=1)
    yes_button = types.InlineKeyboardButton("Да, давай", callback_data='yes')
    markup.add(yes_button)

    bot.send_message(message.chat.id, "Ну что, начнем?", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == "private":
        if message.text == "🔄 Перезапустить бота":
            start(message)
        if message.text == "ℹ️ Помощь в использовании":
            help(message)
        if message.text == "⬅️ Назад":
            request(message)
        if message.text == "▶️ Создать график функции":
            function(message)



@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "yes":
        bot.edit_message_text("Ну что, начнем?", callback.message.chat.id, callback.message.id)
        request(callback.message)


#print help info
@bot.message_handler()
def help(message):
    #back & restart buttons
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    back_button = types.KeyboardButton("⬅️ Назад")
    restart_button = types.KeyboardButton("🔄 Перезапустить бота")
    markup.row(back_button)
    markup.row(restart_button)

    #help info
    bot.send_message(message.chat.id, "Правила корректного использования бота:", reply_markup=markup)


@bot.message_handler()
def request(message):
    bot.send_message(message.chat.id, "Хорошо")
    bot.send_message(message.chat.id, "Просто нажми на кнопку, если хочешь создать график")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    build_button = types.KeyboardButton("▶️ Создать график функции")
    help_button = types.KeyboardButton("ℹ️ Помощь в использовании")
    restart_button = types.KeyboardButton("🔄 Перезапустить бота")
    markup.row(build_button)
    markup.row(help_button)
    markup.row(restart_button)
    bot.send_message(message.chat.id, "Если не знаешь как пользоваться ботом, то тебе поможет кнопка ниже", reply_markup=markup)


@bot.message_handler()
def function(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите функцию, по которой вы хотите построить график")
    bot.register_next_step_handler(message, interval)

@bot.message_handler()
def interval(message):
    function = message.text
    bot.send_message(message.chat.id, "Отлично, теперь введите левую границу интревала")
    bot.register_next_step_handler(message, left_border, function)

@bot.message_handler()
def left_border(message, function):
    left = message.text
    function = function
    bot.send_message(message.chat.id, "Отлично, теперь введите правую границу интревала")
    bot.register_next_step_handler(message, right_border, function, left)

@bot.message_handler()
def right_border(message, function, left):
    right = message.text
    left = left
    function = function
    bot.send_message(message.chat.id, "Отлично, вот график вашей функции")

    fig, ax = plt.subplots()
    ax.set_title(f"f(x) = {function}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(float(left), float(right))
    ax.grid()
    x = np.linspace(float(left), float(right), 100)
    y = eval(function)
    ax.plot(x, y)
    plt.savefig("graph.png")
    image(message)


@bot.message_handler()
def image(message):
    graph = open("graph.png", "rb")
    bot.send_photo(message.chat.id, graph)

bot.infinity_polling()
