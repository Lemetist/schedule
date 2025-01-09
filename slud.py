import schedule
import time
import telebot
import os
from dotenv import load_dotenv
import logging
from telebot import types
from schedule_forms import get_schedule, wb_name
from utils import add_space_after_nechet_ned
from slud_download  import download_file
logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("Токен отсутствует в переменных окружения")

bot = telebot.TeleBot(TOKEN)
download_file()
raspis = wb_name()
schedule_name = None


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    buttons = [types.KeyboardButton(day) for day in days]
    markup.add(*buttons)
    bot.reply_to(message, "Выберите день недели:", reply_markup=markup)

@bot.message_handler(commands=['slud'])
def handle_slud(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in raspis]
    markup.add(*buttons)
    markup.add("/start")
    bot.reply_to(message, "Выберите расписание:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
def handle_day(message):
    global schedule_name
    day_name = message.text
    if schedule_name:
        try:
            formatted_schedule_name = add_space_after_nechet_ned(schedule_name)
            schedule_data = get_schedule(day_name, formatted_schedule_name)
        except KeyError:
            schedule_data = "Расписание не найдено"
    else:
        schedule_data = "Расписание не выбрано /slud"
    bot.reply_to(message, schedule_data)

@bot.message_handler(func=lambda message: message.text in raspis)
def handle_schedule(message):
    global schedule_name
    schedule_name = message.text
    bot.reply_to(message, f"Расписание для {schedule_name}")

bot.polling(none_stop=True)

@bot.message_handler(commands=['download'])
def handle_download(message):
    try:
        download_file()
        bot.reply_to(message, "Файл успешно скачан.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при скачивании файла: {e}")

schedule.every(2).hours.do(download_file)

while True:
    schedule.run_pending()
    time.sleep(1)


