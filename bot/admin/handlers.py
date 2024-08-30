from pyrogram import filters
from pyrogram.types import Message
from pyromod import Client

from bot import config
import bot.db_driver as db
import bot.admin.db_driver as admin_db
from bot.models import AppClient
from bot.static.keyboards import AdminReplyKeyboards, MenuOptions
from bot.static.states import State

app = AppClient.client


def admin_filter(_, client, msg):
    return admin_db.user_is_admin(msg.from_user.id)


is_admin = filters.create(admin_filter)


@app.on_message(filters.regex(config.config['ADMIN_KEY']) & is_admin)
async def admin_start(client: Client, message: Message):
    chat_id = message.chat.id
    await client.send_message(chat_id, 'Welcome admin', reply_markup=AdminReplyKeyboards.START)
    opt = await client.listen(chat_id=chat_id)


async def process(client: Client, msg: Message):
    text = msg.text
    if text == MenuOptions.ADMIN_OPTIONS.CONTACT_USER:
        pending_users = db.get_users_with_state(State.PENDING_MANAGER)
        # TODO choosing option and passing to function


@app.on_message(filters.command('add_lesson') & filters.private)
async def add_lesson(c: Client, msg: Message):
    chat_id = msg.chat.id
    title = await c.ask(chat_id, 'Enter lesson title', filters=filters.private)
    date = await c.ask(chat_id, 'Enter date', filters=filters.private)
    time = await c.ask(chat_id, 'Enter time', filters=filters.private)
    price = await c.ask(chat_id, 'Enter lesson price', filters=filters.private)

    # TODO add saving of lesson
