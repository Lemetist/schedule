import pandas as pd
from utils import add_space_after_nechet_ned, find_closest_sheet_name

def wb_name():
    wb = pd.ExcelFile("1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m.xlsx")
    return [add_space_after_nechet_ned(item.strip()) for item in wb.sheet_names]

def get_schedule(day_name, schedule_name):
    # Загрузка Excel файла
    wb = pd.ExcelFile("1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m.xlsx")
    closest_sheet_name = find_closest_sheet_name(wb.sheet_names, schedule_name)
    if not closest_sheet_name:
        return "Расписание не найдено"

    # Чтение конкретного листа в DataFrame
    df = pd.read_excel(wb, sheet_name=closest_sheet_name, usecols='FV:FX', skiprows=6, nrows=36)

    # Преобразование всех столбцов в тип object
    df = df.astype(object)

    # Заполнение NaN значений "Не указано"
    df.fillna("Не указано", inplace=True)

    # Разделение DataFrame на блоки по 6 строк
    data_by_days = [df.iloc[i:i + 6].values.tolist() for i in range(0, len(df), 6)]

    # Функция для форматирования расписания
    def format_schedule(day_data, day_name):
        formatted_schedule = []
        times = ["08:00 — 09:35", "09:45 — 11:20", "11:50 — 13:25", "13:55 — 15:30", "15:40 — 17:15", "17:25 — 19:00"]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

        for index, row in enumerate(day_data):
            subject = row[0] if len(row) > 0 else "Не указано"
            teacher = row[1] if len(row) > 1 else "Не указано"
            time = times[index] if index < len(times) else "Не указано"
            emoji = emojis[index] if index < len(emojis) else ""
            formatted_schedule.append(f"{emoji} {time} : {subject} ({teacher})")

        return f"Расписание на {day_name}:\n" + "\n".join(formatted_schedule)

    # Дни недели для расписания
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    # Проверка, что day_name входит в список дней недели
    if day_name not in days_of_week:
        return "Неправильный день недели"

    day_index = days_of_week.index(day_name)
    day_data = data_by_days[day_index] if day_index < len(data_by_days) else None
    if not day_data:
        return f"Расписание на {day_name} не найдено"
    return format_schedule(day_data, day_name)