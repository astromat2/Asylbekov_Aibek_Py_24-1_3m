from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp


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
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Это не Эверест)",
        open_period=5,
        reply_markup=markup
    )


# @dp.callback_query_handler(text="button_call_2")
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
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        # open_period=5,
    )



def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="button_call_1")
    dp.register_callback_query_handler(quiz_3, text="button_call_2")