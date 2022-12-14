from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp
from keyboards.client_kb import start_markup


# @dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Приветствую Владыка {message.from_user.first_name}",
                           reply_markup=start_markup)
    # await message.answer("/quiz - атветь на вопросы, проверь насколько ты умный")
    # await message.answer('/mem - мем')
    # await message.answer('Или введи любое число')


async def info_handler(message: types.Message):
    await message.reply("Сам разбирайся!")


async def pin(message: types.Message):
    if not message.reply_to_message:
        await message.reply('команда должна быть ответов на сообщение')
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
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=5,
        reply_markup=markup
    )


async def dice(message: types.Message):
    bot_dice = await bot.send_dice(message.chat.id)
    user_dice = await bot.send_dice(message.chat.id)
    await message.answer("первый игральный кость бота а второй игрока")
    if bot_dice.dice.value > user_dice.dice.value:
        await message.answer(f"Бот выиграл у {message.from_user.full_name}!")
    elif bot_dice.dice.value == user_dice.dice.value:
        await message.answer("Ничья")
    else:
        await message.answer(f"{message.from_user.full_name} выиграл у бота!")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(dice, commands=['dice'])