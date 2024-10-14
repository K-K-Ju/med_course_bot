import logging
import time

from pyrogram import filters
from pyrogram.types import Message
from pyromod import Client

import bot
from bot.db_driver import LessonDb
from bot.user.db_driver import ClientsDb
from bot.admin.db_driver import AdminDb
from bot.models import AppClient, LessonDTO, AdminDTO
from bot.static.keyboards import AdminReplyKeyboards, MenuOptions
from bot.static.states import State

app = AppClient.client
log = logging.getLogger()

__admin_db__: AdminDb = None
__lessons_db__: LessonDb = None
__db__: ClientsDb = None


def inject_dbs(redis_pool):
    global __db__, __lessons_db__, __admin_db__

    __db__ = ClientsDb(redis_pool)
    __lessons_db__ = LessonDb(redis_pool)
    __admin_db__ = AdminDb(redis_pool)


async def admin_start(c: Client, msg: Message):
    chat_id = msg.chat.id
    if __admin_db__.is_admin(chat_id):
        __admin_db__.set_admin_state(chat_id, State.ACTIVE_ADMIN)
    else:
        __admin_db__.add(AdminDTO(chat_id, State.ACTIVE_ADMIN))

    await c.send_message(chat_id, 'Вітаю, адмін!')
    await send_admin_menu(c, msg)


async def send_admin_menu(c: Client, msg: Message):
    chat_id = msg.chat.id
    await c.send_message(msg.chat.id, 'Оберіть пункт меню', reply_markup=AdminReplyKeyboards.START)
    # opt = await c.listen(chat_id=chat_id)
    # await process(c, opt)


async def process(c: Client, msg: Message):
    text = msg.text
    if text == MenuOptions.ADMIN_OPTIONS.CONTACT_USER:
        pending_users = __db__.get_by_state(State.PENDING_MANAGER)
        # TODO choosing option and passing to function
    elif text == MenuOptions.ADMIN_OPTIONS.ADD_LESSON:
        await add_lesson(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.GET_LESSONS:
        await view_lessons(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.EXIT:
        __admin_db__.set_admin_state(msg.from_user.id, State.BASE)
        await c.send_message(msg.chat.id, 'Ви вийшли з панелі адміна')
        await bot.user.handlers.send_menu(c, msg)
        return

    msg.stop_propagation()


async def view_lessons(c: Client, msg: Message):
    lessons = __lessons_db__.get_lessons()
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

    __lessons_db__.add(LessonDTO(title, str_datetime, price, description))

    await c.send_message(chat_id, f'Урок доданий - {title}')
    await send_admin_menu(c, msg)
