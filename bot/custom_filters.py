from pyromod import Client
from pyrogram.types import Message
from pyrogram import filters
import emoji
import bot.admin.db_driver as admin_db


def __emoji_filter__(_, client: Client, msg: Message):
    return emoji.is_emoji(msg.text[0])


first_is_emoji = filters.create(__emoji_filter__)


def __admin_filter__(_, client, msg):
    return admin_db.user_is_admin(msg.from_user.id)


is_admin = filters.create(__admin_filter__)
