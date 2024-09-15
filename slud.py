import telebot
import os
from dotenv import load_dotenv
import logging
from telebot import types
from schedule import get_schedule, wb_name  # Импорт функций для получения расписания

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv('TOKEN')

# Проверка наличия токена
if not TOKEN:
    raise ValueError("Токен отсутствует в переменных окружения")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Загрузка расписания
raspis = wb_name()  # Убедитесь, что wb_name() возвращает список дней или названий расписаний


schedule_name = None
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание кнопок для выбора дня недели
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    buttons = [types.KeyboardButton(day) for day in days]
    markup.add(*buttons)
    bot.reply_to(message, "Выберите день недели:", reply_markup=markup)

# Обработчик команды /slud
@bot.message_handler(commands=['slud'])
def handle_slud(message):
    # Создание кнопок для выбора расписания
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in raspis]
    markup.add(*buttons)
    markup.add("/start")
    bot.reply_to(message, "Выберите расписание:", reply_markup=markup)

# Обработчик текстовых сообщений для дня недели
@bot.message_handler(func=lambda message: message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
def handle_day(message):
    global schedule_name
    day_name = message.text
    schedule_data = get_schedule(day_name,schedule_name)
    bot.reply_to(message, schedule_data)

# Обработчик текстовых сообщений для расписания
@bot.message_handler(func=lambda message: message.text in raspis)
def handle_schedule(message):
    global schedule_name
    schedule_name = message.text
    bot.reply_to(message, f"Расписание для {schedule_name}")

# Запуск бота
bot.polling(none_stop=True)
