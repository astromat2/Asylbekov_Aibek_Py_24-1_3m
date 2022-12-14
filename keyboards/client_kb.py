from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=4
)

start_button = KeyboardButton("/start")
info_button = KeyboardButton("/info")
quiz_button = KeyboardButton("/quiz")
mem_button = KeyboardButton("/mem")

share_location = KeyboardButton("Share location", request_location=True)
share_contact = KeyboardButton("Share contact", request_contact=True)

start_markup.add(start_button, info_button, quiz_button,mem_button,
                 share_location, share_contact)