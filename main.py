import time
from pyrogram import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from art import tprint
from tqdm import tqdm

tprint("Spot catoon cards bot")

seconds = 2
app = Client('my_account',
             api_id=22073531,
             api_hash="6fe3b52911494bff54fd95923a8f1b82")
scheduler = AsyncIOScheduler()
quol = 1


async def get_last_message():
    async for message in app.get_chat_history(chat_id="CartoonSpotBot", limit=1, offset_id=-1):
        return message.text


async def main():
    global seconds, quol
    await app.send_message(chat_id="CartoonSpotBot",
                           text="🧀 Получить карту")
    time.sleep(1)
    message = await get_last_message()
    try:
        if "Следующая попытка будет доступна через" in message and "🧀 Держи свою карту, бро" not in message:
            a = message.split()[5:]
            if "ч" in a:
                seconds = int(a[0]) * 3600 + int(a[2]) * 60 + 60
            else:
                seconds = int(a[0]) * 60 + 60
            scheduler.remove_job("my_job_id")
            scheduler.add_job(main, "interval", seconds=seconds, id="my_job_id")
            text = f'Получение карты {quol}'
            print(text.center(len(text) + 100) + "\n")
            for _ in tqdm(range(seconds)):
                time.sleep(1)

    except TypeError:
        print("Карта получена!")
        quol += 1
        time.sleep(1)
        try:
            with open("data.txt", "a") as file:
                file.write(await get_last_message())
        except Exception as e:
            print(e)

        scheduler.remove_job("my_job_id")
        seconds = 14400
        scheduler.add_job(main, "interval", seconds=seconds, id="my_job_id")
        text = f'Получение карты {quol}'
        print(text.center(len(text) + 100) + "\n")
        for _ in tqdm(range(seconds)):
            time.sleep(1)

if __name__ == '__main__':
    scheduler.add_job(main, "interval", seconds=seconds, id="my_job_id")
    scheduler.start()
    app.run()
#пенис