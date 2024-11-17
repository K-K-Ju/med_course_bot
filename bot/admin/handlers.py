import logging
import re
import time
from typing import List

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyromod import Client

import bot
from bot.db_driver import LessonDb, ApplyDb
from bot.user.db_driver import ClientsDb
from bot.admin.db_driver import AdminDb
from bot.models import AppClient, LessonDTO, AdminDTO
from bot.static.keyboards import AdminReplyKeyboards, MenuOptions
from bot.static.states import State

app = AppClient.client
log = logging.getLogger()

_admin_db_: AdminDb
_lessons_db_: LessonDb
_db_: ClientsDb
_applies_db_: ApplyDb


def inject_dbs(redis_pool):
    global _db_, _lessons_db_, _admin_db_, _applies_db_

    _db_ = ClientsDb(redis_pool)
    _lessons_db_ = LessonDb(redis_pool)
    _admin_db_ = AdminDb(redis_pool)
    _applies_db_ = ApplyDb(redis_pool)


async def admin_start(c: Client, msg: Message):
    chat_id = str(msg.chat.id)
    if _admin_db_.is_admin(chat_id):
        _admin_db_.set_admin_state(chat_id, State.ACTIVE_ADMIN)
    else:
        _admin_db_.add(AdminDTO(chat_id, State.ACTIVE_ADMIN))

    await c.send_message(chat_id, 'Вітаю, адмін!')
    await send_admin_menu(c, msg)


async def send_admin_menu(c: Client, msg: Message):
    chat_id = msg.chat.id
    await c.send_message(msg.chat.id, 'Оберіть пункт меню', reply_markup=AdminReplyKeyboards.START)


async def process(c: Client, msg: Message):
    text = msg.text
    if text == MenuOptions.ADMIN_OPTIONS.ADD_LESSON:
        await add_lesson(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.GET_LESSONS:
        await view_lessons(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.FIND_USER:
        credentials = (await c.ask(msg.chat.id, 'Введіть номер телефону, username або Telegram id')).text
        await retrieve_user_data(c, msg, credentials)
    elif text == MenuOptions.ADMIN_OPTIONS.EXIT:
        _admin_db_.set_admin_state(str(msg.from_user.id), State.BASE)
        await c.send_message(msg.chat.id, 'Ви вийшли з панелі адміна')
        await bot.user.handlers.send_menu(c, msg)
        return

    msg.stop_propagation()


async def view_lessons(c: Client, msg: Message):
    lessons = _lessons_db_.list()
    s = ''
    for l in lessons:
        s += f'{l.title} - {l.datetime} - {l.price}\n'

    await c.send_message(msg.chat.id, s)


async def add_lesson(c: Client, msg: Message):
    chat_id = msg.chat.id
    title = (await c.ask(chat_id, "Введіть назву уроку", filters=filters.private)).text
    while True:
        str_datetime = (await c.ask(chat_id,
                                    'Введіть дату і час проведення у форматі "01.01.2024 10:00"',
                                    filters=filters.private)).text
        if str_datetime == '.':
            break

        try:
            time.strptime(str_datetime, '%d.%m.%Y %H:%M')
            break
        except ValueError:
            log.error(f'Error while parsing datetime from user - {str_datetime}')
            await c.send_message(chat_id, 'Невірний формат дати або часу')

    price = (await c.ask(chat_id, 'Введіть ціну уроку', filters=filters.private)).text
    description = (await c.ask(chat_id, 'Введіть опис уроку', filters=filters.private)).text

    _lessons_db_.add(LessonDTO(title, str_datetime, price, description))

    await c.send_message(chat_id, f'Урок доданий - {title}')
    await send_admin_menu(c, msg)

async def retrieve_user_data(c: Client, msg: Message, credentials: str):
    phone_pattern = r'^\+?3?8?(0-?\d{2}-?\d{3}-?\d{2}-?\d{2})$'
    username_pattern = r"^@\S+$"

    attr = 'id'
    if re.match(phone_pattern, credentials):
        attr = 'phone_number'
    elif re.match(username_pattern, credentials):
        attr = 'username'
        credentials = credentials[1:]

    user = _db_.get_by_attr(attr, credentials)
    user_assignments = _applies_db_.get_by_user_id(user.id)
    assigned_lessons: List[LessonDTO] = []
    for ua in user_assignments:
        assigned_lessons.append(_lessons_db_.get(ua.lesson_id))

    await c.send_message(msg.chat.id,
                         f'**User**:\n\tId: {user.id}\n\t**username**: {user.user_name}\n\t**phone_number**: {user.phone_number}\n\n'+
                         f'Assignments:\n' + '\n'.join([al.title for al in assigned_lessons]),
                         parse_mode=ParseMode.MARKDOWN)