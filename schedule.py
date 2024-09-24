from openpyxl import load_workbook
from utils import add_space_after_nechet_ned, find_closest_sheet_name
from slud_download import download_file
import openpyxl

def wb_name():
    wb = load_workbook("1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m.xlsx")
    return [add_space_after_nechet_ned(item.strip()) for item in wb.sheetnames]

def get_schedule(day_name, schedule_name):
    download_file()
    wb = load_workbook("1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m.xlsx")
    closest_sheet_name = find_closest_sheet_name(wb.sheetnames, schedule_name)
    if not closest_sheet_name:
        return "Расписание не найдено"
    ws = wb[closest_sheet_name]

    min_row, max_row = 8, 43
    min_col_FV = openpyxl.utils.column_index_from_string('FV')
    min_col_FX = openpyxl.utils.column_index_from_string('FX')

    data_combined = [
        [
            ws.cell(row=row, column=min_col_FV).value or "Не указано",
            ws.cell(row=row, column=min_col_FX).value or "Не указано"
        ]
        for row in range(min_row, max_row + 1)
    ]

    def split_into_days(data, num_pairs_per_day):
        return [data[i:i + num_pairs_per_day] for i in range(0, len(data), num_pairs_per_day)]

    data_by_days = split_into_days(data_combined, 6)

    def format_schedule(day_data, day_name):
        times = ["08:00 — 09:35", "09:45 — 11:20", "11:50 — 13:25", "13:55 — 15:30", "15:40 — 17:15", "17:25 — 19:00"]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
        formatted_schedule = [
            f"{emojis[i]} {times[i]} : {subject} ({teacher})"
            for i, (subject, teacher) in enumerate(day_data)
        ]
        return f"Расписание на {day_name}:\n" + "\n".join(formatted_schedule)

    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    if day_name not in days_of_week:
        return "Неправильный день недели"

    day_index = days_of_week.index(day_name)
    day_data = data_by_days[day_index] if day_index < len(data_by_days) else []

    return format_schedule(day_data, day_name)