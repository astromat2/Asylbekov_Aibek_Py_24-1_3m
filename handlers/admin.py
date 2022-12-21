from aiogram import types, Dispatcher
from config import bot
from config import ADMINS
from database.bot_db import sql_command_delete, sql_command_all
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def ban(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение!")
        else:
            await bot.kick_chat_member(message.chat.id,
                                       message.reply_to_message.from_user.id)
            await message.answer(f"{message.from_user.first_name} братан кикнул "
                                 f"{message.reply_to_message.from_user.full_name}")
    else:
        await message.answer("Пиши в группе!")


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой босс!")
    else:
        mentors = await sql_command_all()
        for mentor in mentors:
            await bot.send_message(message.chat.id, f'ID: {mentor[0]}\n'
                                                    f'Name: {mentor[1]}\n'
                                                    f'Direction: {mentor[2]}\n'
                                                    f'Age: {mentor[3]}\n'
                                                    f'Group: {mentor[4]}',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Delete {mentor[1]}', callback_data=f'delete {mentor[0]}')
                                    ))


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Удалено", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))