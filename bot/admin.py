from pyrogram import filters
from pyrogram.types import Message
from pyromod import Client

from bot import config
import bot.db_driver as db
from bot.models.app_client import AppClient

app = AppClient.client


def admin_filter(_, client, msg):
    return db.user_is_admin(msg.from_user.id)


is_admin = filters.create(admin_filter)


@app.on_message(filters.regex(config.config['ADMIN_KEY']) & is_admin)
async def admin_start(client: Client, message: Message):
    await client.send_message(message.chat.id, 'Welcome admin')
