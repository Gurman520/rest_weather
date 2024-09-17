import aiohttp
import asyncio
import dataBase as db


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main():
    url = "https://api.open-meteo.com/v1/forecast?latitude=55.3333&longitude=86.0833&current=apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&wind_speed_unit=ms&timezone=auto&forecast_days=1"  # Замените на ваш API endpoint
    db.init_db()

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url)

        current_data = response.get("current", {})

        if current_data:
            print("Текущие данные:")
            print(f"Ощущаемая температура: {current_data.get('apparent_temperature', 'N/A')} °C")
            print(f"Осадки: {current_data.get('precipitation', 'N/A')} мм")
            print(f"Атмосферное давление: {current_data.get('surface_pressure', 'N/A')} hPa")
            print(f"Скорость ветра: {current_data.get('wind_speed_10m', 'N/A')} м/с")
            print(f"Направление ветра: {current_data.get('wind_direction_10m', 'N/A')} °")
            print(f"Код погоды: {current_data.get('weather_code', 'N/A')} ")

            # Сохранение данных в базу данных
            db.save_to_db(db.SessionLocal, current_data)
        else:
            print("Данные 'current' отсутствуют или пустые")


if __name__ == "__main__":
    asyncio.run(main())
