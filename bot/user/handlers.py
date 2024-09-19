import logging

from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from pyromod import Client
from pyromod.types import ListenerTypes

from bot.models import AppClient
from bot.models import ClientDAO
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.states import State
from bot.user.db_driver import UserDb
from bot.db_driver import LessonDb

logger = logging.getLogger('main_logger')
logger.info('Test logger')
app = AppClient.client
__db__ = UserDb()
__lessons_db__ = LessonDb()


async def send_start(c: Client, msg: Message):
    logger.debug("Received command '/start'")
    await c.send_message(msg.chat.id, Messages.START)
    await send_menu(c, msg)


async def send_menu(c, msg):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    if __db__.exists(msg.from_user.id):
        keyboard = ReplyKeyboards.START

    await c.send_message(msg.chat.id,
                         'Choose desirable option',
                         reply_markup=keyboard)


async def show_status(c, msg: Message):
    user = __db__.get_user(msg.from_user.id)
    # TODO print user status


async def register(c: Client, msg: Message):
    user_id = msg.from_user.id
    if __db__.exists(user_id):
        await c.send_message(msg.chat.id, Messages.USE_MENU_REGISTRATION)
        return

    first_name = (await c.ask(msg.chat.id, 'Enter your name', filters=filters.text)).text
    phone_number = await __get_phone_number__(c, msg)

    app_user = ClientDAO(msg.chat.id,
                         msg.from_user.username, first_name,
                         phone_number, State.BASE)
    __db__.add(app_user)
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


async def __send_lessons_list__(c: Client, chat_id):
    lessons = __lessons_db__.get_lessons()
    for l in lessons:
        await c.send_message(chat_id, f'Title - {l.title}\nPrice - {l.description}',
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton('Записатись', callback_data=f'id={l.id}')]
                             ]))


async def apply(c: Client, query: CallbackQuery):
    id = int(query.data.split('=')[1])


async def answer(c, msg: Message):
    chat_id = msg.chat.id
    if msg.text == MenuOptions.START_MENU.STATUS:
        await c.send_message(chat_id, 'status reply')
    elif msg.text == MenuOptions.START_MENU.APPLY:
        await __send_lessons_list__(c, msg.chat.id)
    elif msg.text == MenuOptions.START_MENU.FAQ:
        await c.send_message(chat_id, 'FAQ option')
    elif msg.text == MenuOptions.START_MENU.REGISTER:
        await register(c, msg)
    elif msg.text == MenuOptions.START_MENU.CONTACT_MANAGER:
        user_id = msg.from_user.id
        __db__.set_state(user_id, State.PENDING_MANAGER)
        await c.send_message(chat_id, 'Wait until manager contacts you via bot')
    elif msg.text == MenuOptions.START_MENU.MENU:
        await send_menu(c, msg)
