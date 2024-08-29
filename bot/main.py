from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import logging

from pyromod.types import ListenerTypes

import db_driver as db
from bot.models.AppUser import AppUser
from bot.models.keyboards import (
    Responses,
    MenuOptions,
    ReplyKeyboards
)
import logger
from bot.models.states import States

logger.prepare_logger(logging.INFO)
logger = logging.getLogger('main_logger')

logger.info('Test logger')
app = Client("Surgeon Course Bot", lang_code='ua')
db.test_db()


@app.on_message(filters.command('start') & filters.private)
async def send_start(client: Client, message: Message):
    logger.debug("Received command '/start'")
    await client.send_message(message.chat.id, Responses.START)
    await send_menu(client, message)


@app.on_message(filters.command('menu') & filters.private)
async def send_menu(client, message):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    if await db.user_exists(message.from_user.id):
        keyboard = ReplyKeyboards.START

    await client.send_message(message.chat.id,
                              'Choose desirable option',
                              reply_markup=keyboard)


@app.on_message(filters.command('status'))
async def show_status(client, message: Message):
    user = await db.get_user(message.from_user.id)
    # TODO print user status


@app.on_message(filters.regex(MenuOptions.START_MENU.REGISTER))
async def register(client: Client, message: Message):
    user_id = message.from_user.id
    if await db.user_exists(user_id):
        await client.send_message(message.chat.id, 'You are already registered. For better experience use menu.')
        return

    first_name = (await client.ask(message.chat.id, 'Enter your name', filters=filters.text)).text
    phone_number = await get_phone_number(client, message)
    app_user = AppUser(user_id, message.chat.id, message.from_user.username, first_name, phone_number, States.REGISTERED)
    db.add_user(app_user)
    logger.debug(f"Registered new user id={user_id}")
    await client.send_message(message.chat.id, 'You are now registered')
    await send_menu(client, message)
    # gs = Gsheet(config_file_name='.gspread_config/med-school-bot-ab94c6ed2675.json',
    # sheet_key='1UNEWjM2tGdSAUdbeBjrIoRlr2P6Q1Iwc7bKscntKe70')


@app.on_message(filters.text & filters.private)
async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.START_MENU.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.START_MENU.APPLY:
        await client.send_message(chat_id, 'attending reply')
    elif message.text == MenuOptions.START_MENU.FAQ:
        await client.send_message(chat_id, 'FAQ option')
    else:
        await client.send_message(chat_id, 'Please choose option in menu')


async def get_phone_number(client, message):
    if message.contact:
        return message.contact.phone_number
    else:
        await message.reply(
            text="Allow to view your phone",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Share mobile", request_contact=True)],
                ],
                resize_keyboard=True,
            ),
        )
        contact_msg = await client.listen(chat_id=message.chat.id, filters=filters.contact, listener_type=ListenerTypes.MESSAGE)
        return contact_msg.contact.phone_number

app.run()
