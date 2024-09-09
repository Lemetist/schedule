import telebot
import os
from dotenv import load_dotenv
import logging
from telebot import types
from schedule import get_schedule  # Импортируем функцию для получения расписания

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv('TOKEN')

# Проверка наличия токена
if not TOKEN:
    raise ValueError("Token is missing from environment variables")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание кнопок для выбора дня недели
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    buttons = [types.KeyboardButton(day) for day in days]
    markup.add(*buttons)
    bot.reply_to(message, "Выберите день недели:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
def handle_day(message):
    day_name = message.text
    schedule_data = get_schedule(day_name)
    bot.reply_to(message, schedule_data)

# Запуск бота
bot.polling(none_stop=True)
