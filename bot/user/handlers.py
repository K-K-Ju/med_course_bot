import logging

from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pyromod import Client
from pyromod.types import ListenerTypes

from bot.models import AppClient
from bot.models import AppUserDAO
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.states import State
from bot.user import db_driver

logger = logging.getLogger('main_logger')
logger.info('Test logger')
app = AppClient.client
db = db_driver.Db()


async def send_start(c: Client, msg: Message):
    logger.debug("Received command '/start'")
    await c.send_message(msg.chat.id, Messages.START)
    await send_menu(c, msg)


async def send_menu(c, msg):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    if db.user_exists(msg.from_user.id):
        keyboard = ReplyKeyboards.START

    await c.send_message(msg.chat.id,
                         'Choose desirable option',
                         reply_markup=keyboard)


async def show_status(c, msg: Message):
    user = db.get_user(msg.from_user.id)
    # TODO print user status


async def register(c: Client, msg: Message):
    user_id = msg.from_user.id
    if db.user_exists(user_id):
        await c.send_message(msg.chat.id, Messages.USE_MENU_REGISTRATION)
        return

    first_name = (await c.ask(msg.chat.id, 'Enter your name', filters=filters.text)).text
    phone_number = await __get_phone_number__(c, msg)

    app_user = AppUserDAO(user_id, msg.chat.id,
                          msg.from_user.username, first_name,
                          phone_number, State.BASE)
    db.add_user(app_user)
    logger.debug(f'Registered new user id={user_id}')
    await c.send_message(msg.chat.id, 'You are now registered')
    await send_menu(c, msg)


async def __get_phone_number__(c, msg):
    if msg.contact:
        return msg.contact.phone_number
    else:
        await msg.reply(
            text='Allow to view your phone',
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Share mobile', request_contact=True)],
                ],
                resize_keyboard=True,
            ),
        )
        contact_msg = await c.listen(chat_id=msg.chat.id, filters=filters.contact,
                                     listener_type=ListenerTypes.MESSAGE)
        return contact_msg.contact.phone_number


async def answer(c, msg: Message):
    chat_id = msg.chat.id
    if msg.text == MenuOptions.START_MENU.STATUS:
        await c.send_message(chat_id, 'status reply')
    elif msg.text == MenuOptions.START_MENU.APPLY:
        await c.send_message(chat_id, 'attending reply')
    elif msg.text == MenuOptions.START_MENU.FAQ:
        await c.send_message(chat_id, 'FAQ option')
    elif msg.text == MenuOptions.START_MENU.REGISTER:
        await register(c, msg)
    elif msg.text == MenuOptions.START_MENU.CONTACT_MANAGER:
        user_id = msg.from_user.id
        db.set_user_state(user_id, State.PENDING_MANAGER)
        await c.send_message(chat_id, 'Wait until manager contacts you via bot')
    elif msg.text == MenuOptions.START_MENU.MENU:
        await send_menu(c, msg)
