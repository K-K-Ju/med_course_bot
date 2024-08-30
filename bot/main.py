import logging

from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pyromod import Client
from pyromod.types import ListenerTypes

import db_driver as db
from bot.models import app_client
from bot.models import AppUser
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.states import State

logger = logging.getLogger('main_logger')
logger.info('Test logger')
app = app_client.AppClient.client


@app.on_message(filters.command('start') & filters.private)
async def send_start(client: Client, message: Message):
    logger.debug("Received command '/start'")
    await client.send_message(message.chat.id, Messages.START)
    await send_menu(client, message)


@app.on_message(filters.command('menu') & filters.private)
async def send_menu(client, message):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    if db.user_exists(message.from_user.id):
        keyboard = ReplyKeyboards.START

    await client.send_message(message.chat.id,
                              'Choose desirable option',
                              reply_markup=keyboard)
    opt = await app.listen(chat_id=message.chat.id, filters=filters.text)
    await answer(client, opt)


@app.on_message(filters.command('status'))
async def show_status(client, message: Message):
    user = db.get_user(message.from_user.id)
    # TODO print user status


async def register(client: Client, message: Message):
    user_id = message.from_user.id
    if db.user_exists(user_id):
        await client.send_message(message.chat.id, 'You are already registered. For better experience use menu.')
        return

    first_name = (await client.ask(message.chat.id, 'Enter your name', filters=filters.text)).text
    phone_number = await get_phone_number(client, message)
    app_user = AppUser(user_id, message.chat.id, message.from_user.username, first_name, phone_number,
                       State.REGISTERED)
    db.add_user(app_user)
    logger.debug(f"Registered new user id={user_id}")
    await client.send_message(message.chat.id, 'You are now registered')
    await send_menu(client, message)


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
        contact_msg = await client.listen(chat_id=message.chat.id, filters=filters.contact,
                                          listener_type=ListenerTypes.MESSAGE)
        return contact_msg.contact.phone_number


async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.START_MENU.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.START_MENU.APPLY:
        await client.send_message(chat_id, 'attending reply')
    elif message.text == MenuOptions.START_MENU.FAQ:
        await client.send_message(chat_id, 'FAQ option')
    elif message.text == MenuOptions.START_MENU.REGISTER:
        await register(client, message)
    elif message.text == MenuOptions.START_MENU.CONTACT_MANAGER:
        user_id = message.from_user.id
        db.set_user_state(user_id, State.PENDING_MANAGER)
        await client.send_message(chat_id, 'Wait until manager contacts you via bot')
    else:
        await client.send_message(chat_id, 'Please choose option in menu')
        await send_menu(client, message)


app.run()
