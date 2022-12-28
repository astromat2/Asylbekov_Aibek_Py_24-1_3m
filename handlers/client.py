from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp
from keyboards.client_kb import start_markup
import random
from database.bot_db import sql_command_random
from par.game import parser


# @dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    # await bot.send_message(chat_id=message.chat.id,
    #                        text=f"Приветствую Владыка {message.from_user.first_name}",
    #                        reply_markup=start_markup)

    await bot.send_message(chat_id=message.chat.id,
                           text=f"Приветствую Владыка {message.from_user.first_name}")
    await message.answer("/quiz - атветь на вопросы, проверь насколько ты умный")
    await message.answer('/mem - мем')
    await message.answer('/reg - Регистрация на менторство')
    await message.answer('/dice - Игральная кость')
    await message.answer('Или введи любое число')


async def info_handler(message: types.Message):
    await message.reply("Сам разбирайся!")


async def pin(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Команда должна быть ответом на сообщение.')
    else:
        await bot.pin_chat_message(message.chat.id, message.message_id)


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
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=5,
        reply_markup=markup
    )


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


async def dice(message: types.Message):
    bot_dice = await bot.send_dice(message.chat.id)
    user_dice = await bot.send_dice(message.chat.id)
    await message.answer("Первая игральная кость бота, а вторая игрока")
    if bot_dice.dice.value > user_dice.dice.value:
        await message.answer(f"Бот выиграл у {message.from_user.full_name}!")
    elif bot_dice.dice.value == user_dice.dice.value:
        await message.answer("Ничья")
    else:
        await message.answer(f"{message.from_user.full_name} выиграл у бота!")


async def get_games(message: types.Message):
    game = parser()
    for i in game:
        await message.answer(
            f"{i['image']}\n"
            f"{i['title']}\n"
            f"{i['link']}\n"
            f"{i['date']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(dice, commands=['dice'])
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(get_games, commands=['Games'])
