import requests


def download_file():
    # ID документа Google Sheets
    doc_id = "1PtRes1tt6fDTc34EtTLN03NizjNZwxWk"

    # URL для экспорта таблицы в формате Excel
    url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=xlsx'

    # Загрузка файла
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Сохранение файла на диск
        file_path = f'{doc_id}.xlsx'
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Ошибка загрузки файла: {response.status_code}')

download_file()

