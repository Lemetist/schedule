import re
from difflib import get_close_matches

def add_space_after_nechet_ned(text):
    # Удаляем лишние пробелы и приводим текст к единому формату
    text = re.sub(r'\s+', ' ', text).strip()

    # Добавляем пробел после "нечетн" и "четн", если его нет
    text = re.sub(r'(нечетн)(?=[^ ])', r'\1 ', text)
    text = re.sub(r'(четн)(?=[^ ])', r'\1 ', text)

    return text

def find_closest_sheet_name(sheet_names, target_name):
    # Находим наиболее близкое совпадение
    closest_matches = get_close_matches(target_name, sheet_names, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None