from openpyxl import Workbook


def get_weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear, partly cloudy, and overcast",
        2: "Mainly clear, partly cloudy, and overcast",
        3: "Mainly clear, partly cloudy, and overcast",
        45: "Fog and depositing rime fog",
        48: "Fog and depositing rime fog",
        51: "Drizzle: Light, moderate, and dense intensity",
        53: "Drizzle: Light, moderate, and dense intensity",
        55: "Drizzle: Light, moderate, and dense intensity",
        56: "Freezing Drizzle: Light and dense intensity",
        57: "Freezing Drizzle: Light and dense intensity",
        61: "Rain: Slight, moderate and heavy intensity",
        63: "Rain: Slight, moderate and heavy intensity",
        65: "Rain: Slight, moderate and heavy intensity",
        66: "Freezing Rain: Light and heavy intensity",
        67: "Freezing Rain: Light and heavy intensity",
        71: "Snow fall: Slight, moderate, and heavy intensity",
        73: "Snow fall: Slight, moderate, and heavy intensity",
        75: "Snow fall: Slight, moderate, and heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight, moderate, and violent",
        81: "Rain showers: Slight, moderate, and violent",
        82: "Rain showers: Slight, moderate, and violent",
        85: "Snow showers slight and heavy",
        86: "Snow showers slight and heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight and heavy hail",
        99: "Thunderstorm with slight and heavy hail"
    }

    return descriptions.get(code, "Unknown weather code")


def degrees_to_direction(degrees):
    directions = ["С", "СВ", "В", "ЮВ",
                  "Ю", "ЮЗ", "З", "СЗ"]
    index = int((int(degrees) + 22.5) / 45) % 8
    return directions[index]


def records_to_xlsx(records, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Current Weather"

    # Заголовки таблицы
    columns = ["ID", "Time", "Apparent Temperature", "Precipitation Value", "Precipitation",
               "Surface Pressure", "Wind Speed", "Wind Direction"]
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
