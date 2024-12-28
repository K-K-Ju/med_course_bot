from dependency_injector.wiring import inject, Provide
from pyromod import Client
from pyrogram.types import Message
from pyrogram import filters
import emoji

from bot.di import DbContainer
from bot.static.enums.states import State


def __emoji_filter__(_, c: Client, msg: Message):
    return emoji.is_emoji(str(msg.text)[0])


first_is_emoji = filters.create(__emoji_filter__)

@inject
def is_admin(db = Provide[DbContainer.admin_db]):
    async def func(flt, _, msg):
        user_id = msg.from_user.id
        return flt.db.is_admin(user_id) & (flt.db.get_state(user_id) == State.ACTIVE_ADMIN)

    return filters.create(func, db=db)

