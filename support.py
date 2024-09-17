from openpyxl import Workbook


def get_weather_description(code) -> str:
    '''
    Функция преобразования кода погоды в текстовое представление
    :param code: число - код погоды
    :return: строковое представление погоды
    '''
    descriptions = {
        0: "Нет осадков",
        1: "Нет осадков",
        2: "Нет осадков",
        3: "Нет осадков",
        45: "Иней",
        48: "Иней",
        51: "Слабый моросящий дождь",
        53: "Не сильный моросящий дождь",
        55: "Сильный моросящий дождь",
        56: "Слабый ледяной моросящий дождь",
        57: "Сильный ледяной моросящий дождь",
        61: "Дождь",
        63: "Дождь",
        65: "Дождь",
        66: "Ледяной дождь",
        67: "Ледяной дождь",
        71: "Снег",
        73: "Снег",
        75: "Снег",
        77: "Снег",
        80: "Ливень",
        81: "Ливень",
        82: "Ливень",
        85: "Снегопад слабый",
        86: "Снегопад сильный",
        95: "Гроза",
        96: "Гроза с небольшим градом",
        99: "Гроза с сильным градом"
    }

    return descriptions.get(code, "Не известная погода")


def degrees_to_direction(degrees) -> str:
    '''
    Функция преобразования градусов в текстовое направление
    :param degrees: Число - Градус направления ветра
    :return: Строка содержащая направление ветра
    '''
    directions = ["С", "СВ", "В", "ЮВ",
                  "Ю", "ЮЗ", "З", "СЗ"]
    index = int((int(degrees) + 22.5) / 45) % 8
    return directions[index]


def records_to_xlsx(records, filename) -> None:
    '''
    Функция преобразования данных в файл с расширением xlsx
    :param records: Данные полученые из базы
    :param filename: Имя файла в который сохрнаить отчет
    :return: None
    '''
    wb = Workbook()
    ws = wb.active
    ws.title = "Current Weather"

    # Заголовки таблицы
    columns = ["ID", "Время", "Температура", "Количество осадков", "Тип осадков",
               "Давление воздуха", "Скорость ветра", "Направление ветра"]
    ws.append(columns)

    for record in records:
        row = [
            record.id,
            record.time,
            record.apparent_temperature,
            record.precipitation_value,
            record.precipitation,
            record.surface_pressure,
            record.wind_speed,
            record.wind_direction
        ]
        ws.append(row)
    wb.save(filename)
