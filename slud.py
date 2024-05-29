from main import schedule_dataz
import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

# Получаем данные о расписании
schedule_dataz_result = schedule_dataz()
schedule_data = {
    "Понедельник": schedule_dataz_result[0],
    "Вторник": schedule_dataz_result[1],
    "Среда": schedule_dataz_result[2],
    "Четверг": schedule_dataz_result[3],
    "Пятница": schedule_dataz_result[4],
    "Суббота": schedule_dataz_result[5]
}

# Функция для форматирования расписания
def format_schedule(schedule):
    formatted_schedule = ""
    for i, item in enumerate(schedule, start=1):
        if item:
            # Удаляем символы [, ], и \n
            cleaned_item = [line.replace('[', '').replace(']', '').replace('\n', '') for line in item]
            formatted_schedule += f"{i}️⃣ {''.join(cleaned_item)}\n\n"
    return formatted_schedule.strip()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [types.KeyboardButton(day) for day in schedule_data.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Привет! Чтобы узнать расписание, выбери день недели:", reply_markup=markup)

# Обработчик кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text in schedule_data:
        schedule = schedule_data[message.text]
        formatted_schedule = format_schedule(schedule)
        if formatted_schedule:
            bot.send_message(message.chat.id, f"Расписание на {message.text}:\n{formatted_schedule}")
        else:
            bot.send_message(message.chat.id, f"На {message.text} занятий нет.")
    else:
        bot.send_message(message.chat.id, "Выбери день недели из списка.")

# Запуск бота
bot.polling()
