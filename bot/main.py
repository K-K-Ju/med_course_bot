from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

import logging
import db_driver
from bot.Gsheet import Gsheet
from bot.models.keyboards import (
    Responses,
    MenuOptions,
    ReplyKeyboards, Level
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
    if message.chat.type == ChatType.PRIVATE:
        user = message.from_user
        user_id, username = user.id, user.username
        if not db_driver.user_exists(user_id):
            db_driver.add_client(user_id, username, message.chat.id)
            logger.debug(f"Added new {username=}")

    user = db_driver.get_user(message.from_user.id)
    gs = Gsheet(config_file_name='.gspread_config/med-school-bot-ab94c6ed2675.json',
                sheet_key='1UNEWjM2tGdSAUdbeBjrIoRlr2P6Q1Iwc7bKscntKe70')
    await gs.add_user(user)  # TODO test gsheet add user
    keyboard = ReplyKeyboards.START

    await client.send_message(message.chat.id,
                              Responses.START,
                              reply_markup=keyboard)


@app.on_message(filters.command('status'))
async def show_status(client, message: Message):
    db_driver.get_user(message.from_user.id)
    # TODO print user status


@app.on_message(filters.text & filters.private)
async def answer(client, message: Message):
    chat_id = message.chat.id
    if message.text == MenuOptions.START_MENU.STATUS:
        await client.send_message(chat_id, 'status reply')
    elif message.text == MenuOptions.START_MENU.APPLY:
        await client.send_message(chat_id, 'attending reply')
    elif message.text == MenuOptions.START_MENU.FAQ:
        await choose(client, message, dict(MenuOptions.START_MENU.__dict__))


async def process_faq(client, msg: Message, level: Level):
    lvl_num = int(level.__class__.__name__[:-1])
    try:
        next_lvl = eval(f'Level{lvl_num+1}')
    except KeyError:
        logger.error(f'No menu level with number {lvl_num+1=}')
        await client.send_message(Responses.BACK)
    while msg.text != Responses.BACK:
        await choose(client, msg, next_lvl)
        pass
    # determine LEVEL -> decrement level -> process_faq


async def choose(client: Client, msg: Message, options: dict):
    option_name = list(options.keys())[list(options.values()).index(msg.text)]

    keyboards_dict = ReplyKeyboards.__dict__
    keyboards = dict(list(keyboards_dict.items())[1:-3])

    keyboard = keyboards.get(option_name)
    gl = globals()
    # next_options_name = f'{module}.ReplyKeyboards.{option_name}_OPTIONS'

    next_options = eval(f'dict(MenuOptions.{option_name}_OPTIONS.__dict__)')

    await client.send_message(msg.chat.id, text='Choose question', reply_markup=keyboard)
    new_msg = await client.listen(chat_id=msg.chat.id, filters=filters.text)
    if new_msg.text == Responses.BACK:
        return

    await choose(client, new_msg, next_options)


app.run()
