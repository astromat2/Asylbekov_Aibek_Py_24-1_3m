from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS
from keyboards import client_kb
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMINS:
        await FSMAdmin.id.set()
        await message.answer(f'Приветствую {message.from_user.full_name}\n'
                             f'Напиши свой ID', reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пиши в личке!")


async def load_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['id'] = int(message.text)

        await FSMAdmin.next()
        await message.answer("Имя?", reply_markup=client_kb.cancel_markup)

    except:
        await bot.send_message(message.from_user.id, "ID должен состоять из цифр!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Направление?", reply_markup=client_kb.cancel_markup)


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Возраст?", reply_markup=client_kb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа!", reply_markup=client_kb.cancel_markup)
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Какая группа?", reply_markup=client_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(f"ID: {data['id']}\n"
                             f"Имя: {data['name']}\n"
                             f"Направление: {data['direction']}\n"
                             f"Возраст: {data['age']}\n"
                             f"Группа: {data['group']}\n")
    await FSMAdmin.next()
    await message.answer("Все правильно?", reply_markup=client_kb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
        await message.answer("Ты теперь ментор будешь рубить капусту😏")
    elif message.text.lower() == "нет":
        await state.finish()
        await message.answer("Ну и пошел ты!")
    else:
        await message.answer('НИПОНЯЛ!?')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Не хочет быть ментором 😔", reply_markup=client_kb.start_markup)


def register_handlers_fsm_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
