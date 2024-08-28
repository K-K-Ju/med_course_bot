from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message

import logging
import db_driver
from bot.models.AppUser import AppUser
from bot.models.keyboards import (
    Responses,
    MenuOptions,
    ReplyKeyboards
)
import logger

logger.prepare_logger(logging.INFO)
logger = logging.getLogger('main_logger')

logger.info('Test logger')
app = Client("Surgeon Course Bot", lang_code='ua')
db_driver.prepare_db()


@app.on_message(filters.command('start') & filters.private)
async def send_start(client: Client, message):
    logger.debug("Received command '/start'")

    keyboard = ReplyKeyboards.START
    await client.send_message(message.chat.id,
                              Responses.START,
                              reply_markup=keyboard)


@app.on_message(filters.command('status'))
async def show_status(client, message: Message):
    user = await db_driver.get_user(message.from_user.id)
    # TODO print user status


@app.on_message(filters.text & filters.private)
async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.START_MENU.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.START_MENU.APPLY:
        await client.send_message(chat_id, 'attending reply')
    elif message.text == MenuOptions.START_MENU.FAQ:
        await client.send_message(chat_id, 'FAQ option')


async def register(app_user: AppUser):
    if not db_driver.user_exists(app_user.user_id):
        db_driver.add_client(app_user)
        logger.debug(f"Registered new user id={app_user.user_id}")

    # gs = Gsheet(config_file_name='.gspread_config/med-school-bot-ab94c6ed2675.json',
    # sheet_key='1UNEWjM2tGdSAUdbeBjrIoRlr2P6Q1Iwc7bKscntKe70')


app.run()