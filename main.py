import aiohttp
import threading
import asyncio
import time
import dataBase as db
from support import records_to_xlsx


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def periodic_api_call(url, interval):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                response = await fetch(session, url)  # делаем запрос
                current_data = response.get("current", {})  # Достаем нужные данные
                db.save_to_db(db.SessionLocal, current_data)  # Сохраняем в БД
            except Exception as e:
                print(f"Error during API call: {e}")
            await asyncio.sleep(interval)


def handle_user_input():
    while True:
        print("Чтобы выгрузить отчет, введите команду - download to excel\nЧтобы завершить работу, введите - exit")
        user_input = input("Enter your command: ")
        time.sleep(1)
        if user_input.lower() == "download to excel":
            print("Начинаю выгрузку отчета")
            records_to_xlsx(db.get_last_10_records(session=db.SessionLocal), "output.xlsx")
            print("Выгрузка отчета успешно завершена")

        elif user_input.lower() == "exit":
            print("Завершение программы...")
            exit()


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    url = "https://api.open-meteo.com/v1/forecast?latitude=55.3333&longitude=86.0833&current=apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&wind_speed_unit=ms&timezone=auto&forecast_days=1"  # Замените на ваш API endpoint
    db.init_db()
    interval = 10  # 3 minutes

    # Создаем новый событийный цикл для выполнения асинхронных задач
    new_loop = asyncio.new_event_loop()

    # Запускаем событийный цикл в новом потоке
    fetcher_thread = threading.Thread(target=start_event_loop, args=(new_loop,), daemon=True)
    fetcher_thread.start()

    # Запускаем асинхронную задачу в новом событийном цикле
    asyncio.run_coroutine_threadsafe(periodic_api_call(url, interval), new_loop)

    handle_user_input()


if __name__ == "__main__":
    main()
