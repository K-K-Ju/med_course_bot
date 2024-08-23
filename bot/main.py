from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message
)

import logging
import db_driver
from bot.models.keyboards import Responses, MenuOptions, ReplyKeyboards
import logger

logger.prepare_logger(logging.INFO)
logger = logging.getLogger('main_logger')

logger.info('Test logger')
app = Client("Surgeon Course Bot", lang_code='ua')
db_driver.prepare_db()


@app.on_message(filters.command('start') & filters.private)
async def send_start(client: Client, message):
    logger.debug("Received command '/start'")
    if message.chat.type == ChatType.PRIVATE:
        user = message.from_user
        user_id, username = user.id, user.username
        if not db_driver.user_exists(user_id):
            db_driver.add_client(user_id, username, message.chat.id)
            logger.debug(f"Added new {username=}")

    user = db_driver.get_user(message.from_user.id)

    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.STATUS)],
        [KeyboardButton(MenuOptions.APPLY)],
        [KeyboardButton(MenuOptions.FAQ)],
    ], is_persistent=True, placeholder='Choose option in menu', resize_keyboard=True)

    await client.send_message(message.chat.id,
                              Responses.START,
                              reply_markup=keyboard)


@app.on_message(filters.command('status'))
async def show_status(client, message: Message):
    db_driver.get_user(message.from_user.id)


@app.on_message(filters.text & filters.private)
async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.APPLY:
        await client.send_message(chat_id, 'attending reply')
    elif message.text == MenuOptions.FAQ:
        await handle_faq_menu(client, message)


async def handle_faq_menu(client: Client, message):
    logger.debug('Handling FAQ conversation')
    chat_id = message.chat.id
    keyboard = ReplyKeyboards.QUESTIONS
    await client.send_message(chat_id, text='Choose question', reply_markup=keyboard)
    msg: Message = await client.listen(chat_id=chat_id, filters=filters.text)
    msg_txt = msg.text
    if msg_txt == ReplyKeyboards.QuestionsOptions.ABOUT_SCHOOL:
        logger.debug('Option ABOUT_SCHOOL')
        keyboard = ReplyKeyboards.ABOUT_SCHOOL
        await client.send_message(chat_id, text='Choose option', reply_markup=keyboard)
    elif msg_txt == ReplyKeyboards.QuestionsOptions.MONEY:
        logger.debug('Option MONEY')
        await client.send_message(chat_id, text='Choose option')
    elif msg_txt == ReplyKeyboards.QuestionsOptions.WHO_SUITS:
        logger.debug('Option WHO_SUITS')
        await client.send_message(chat_id, text='Choose option')


app.run()
