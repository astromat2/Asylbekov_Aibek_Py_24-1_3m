import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await message.answer("Будет сделано!")


async def go_to_GeekTech():
    await bot.send_message(chat_id=chat_id, text="Теперь можно оставаться на ночь в коворкинге!")


async def scheduler():
    aioschedule.every().tuesday.at('17:30').do(go_to_GeekTech)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


async def indusy():
    await bot.send_message(chat_id=chat_id, text="Пора смотреть как индусы строят дома из глины")


async def scheduler():
    aioschedule.every().saturday.at('03:00').do(indusy)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_id, lambda word: "напомни" in word.text)