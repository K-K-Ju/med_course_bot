from pyrogram import filters
from pyrogram.types import Message
from pyromod import Client

from bot.custom_filters import first_is_emoji
from bot import config
import bot.db_driver as db
import bot.admin.db_driver as admin_db_driver
from bot.models import AppClient, LessonDAO
from bot.static.keyboards import AdminReplyKeyboards, MenuOptions
from bot.static.states import State
from bot.custom_filters import is_admin

app = AppClient.client
admin_db = admin_db_driver.AdminDb()


@app.on_message(filters.regex(config.config['ADMIN_KEY']) & is_admin)
async def admin_start(c: Client, msg: Message):
    chat_id = msg.chat.id
    await c.send_message(chat_id, 'Welcome admin')
    await send_menu(c, msg)


async def send_menu(c: Client, msg: Message):
    chat_id = msg.chat.id
    await c.send_message(msg.chat.id, 'Choose option', reply_markup=AdminReplyKeyboards.START)
    opt = await c.listen(chat_id=chat_id)
    await process(c, opt)


@app.on_message(filters.text & filters.private & first_is_emoji)
async def process(c: Client, msg: Message):
    text = msg.text
    if text == MenuOptions.ADMIN_OPTIONS.CONTACT_USER:
        pending_users = db.get_users_with_state(State.PENDING_MANAGER)
        # TODO choosing option and passing to function
    elif text == MenuOptions.ADMIN_OPTIONS.ADD_LESSON:
        await add_lesson(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.GET_LESSONS:
        await view_lessons(c, msg)

    await send_menu(c, msg)


async def view_lessons(c: Client, msg: Message):
    lessons = admin_db.get_lessons()
    print(lessons)


async def add_lesson(c: Client, msg: Message):
    chat_id = msg.chat.id
    title = (await c.ask(chat_id, 'Enter lesson title', filters=filters.private)).text
    date = (await c.ask(chat_id, 'Enter date', filters=filters.private)).text
    time = (await c.ask(chat_id, 'Enter time', filters=filters.private)).text
    price = (await c.ask(chat_id, 'Enter lesson price', filters=filters.private)).text
    description = (await c.ask(chat_id, 'Enter lesson description', filters=filters.private)).text
    admin_db.add_lesson(LessonDAO(title, date, time, price, description))

    await c.send_message(chat_id, 'Lesson added')
