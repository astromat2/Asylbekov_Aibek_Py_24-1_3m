from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import logging
import random

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Приветствую Владыка {message.from_user.first_name}")
    await message.answer("/quiz - атветь на вопросы, проверь насколько ты умный")
    await message.answer('/mem - мем')
    await message.answer('Или введи любое число')
    # await message.reply("This is a reply method")


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT 1", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Какая служба электронной почты принадлежит компании Microsoft?"
    answers = [
        'Outlook',
        'Yahoo Mail',
        'Gmail',
        'iCloud Mail',
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=5,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT 2", callback_data="button_call_2")
    markup.add(button_call_1)

    question = "Самая высокая гора в мире если не измерять от уровня моря"
    answers = [
        "Ала-Тоо",
        "Эверест",
        "Гималаи",
        "Мауна-Кеа",
        "Канченджанга",
        "Фудзи",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Это не Эверест)",
        open_period=5,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_call_2")
async def quiz_3(call: types.CallbackQuery):
    question = "На каком языке больше всего слов"
    answers = [
        'Китайский',
        'Английский',
        'Русский',
        'Французский',
        'Японский',
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        # open_period=5,
    )

@dp.message_handler(commands=['mem'])
async def mem(message: types.Message):
    mems = [
        'media/mem1.jpg',
        'media/mem2.jpg',
        'media/mem3.jpg',
        'media/mem4.jpg',
        'media/mem5.jpg'
    ]
    mem = open(random.choice(mems), 'rb')
    await bot.send_photo(message.chat.id, photo=mem)


@dp.message_handler()
async def echo(message: types.Message):
    # print(message)
    await bot.send_message(chat_id=message.from_user.id, text=message.text)
    a = int(message.text)
    if a:
        await bot.send_message(chat_id=message.from_user.id, text=a ** 2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)