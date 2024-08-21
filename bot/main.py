from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message
)

import logging
import db_driver
from bot.models.static import Responses, MenuOptions
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

    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.STATUS)],
        [KeyboardButton(MenuOptions.APPLY)],
        [KeyboardButton(MenuOptions.FAQ)],
    ], is_persistent=True, placeholder='Choose option in menu')

    await client.send_message(message.chat.id,
                              Responses.START,
                              reply_markup=keyboard)


@app.on_message(filters.me)
async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.APPLY:
        await client.send_message(chat_id, 'attending reply')
    else:
        await client.send_message(chat_id, 'faq reply')


app.run()
