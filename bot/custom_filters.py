from pyromod import Client
from pyrogram.types import Message
from pyrogram import filters
import emoji
import bot.admin.db_driver as admin_db_driver
from bot.static.states import State


def __emoji_filter__(_, client: Client, msg: Message):
    return emoji.is_emoji(str(msg.text)[0])


first_is_emoji = filters.create(__emoji_filter__)


def __admin_filter__(_, client, msg):
    admin_db = admin_db_driver.AdminDb()
    user_id = msg.from_user.id
    return admin_db.user_is_admin(user_id) & (admin_db.get_state(user_id) == State.ACTIVE_ADMIN)


is_admin = filters.create(__admin_filter__)
