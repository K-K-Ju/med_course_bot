import logging
import re
import time
from typing import List

from dependency_injector.wiring import inject, Provide
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyromod import Client

import bot
from bot.di import DbContainer
from bot.models.dto.admin import AdminDTO
from bot.models.app_client import AppClient
from bot.models.dto.lesson import LessonDTO
from bot.static.keyboards import AdminReplyKeyboards, MenuOptions
from bot.static.enums.states import State

app = AppClient.client
log = logging.getLogger()


@inject
async def admin_start(c: Client, msg: Message,
                      admins_db=Provide[DbContainer.admin_db]):
    chat_id = str(msg.chat.id)
    if admins_db.is_admin(chat_id):
        admins_db.set_admin_state(chat_id, State.ACTIVE_ADMIN)
    else:
        admins_db.add(AdminDTO(chat_id=chat_id, state=State.ACTIVE_ADMIN))

    await c.send_message(chat_id, "Вітаю, адмін!")
    await send_admin_menu(c, msg)


async def send_admin_menu(c: Client, msg: Message):
    await c.send_message(msg.chat.id, "Оберіть пункт меню", reply_markup=AdminReplyKeyboards.START)


@inject
async def process(c: Client, msg: Message,
                  admins_db=Provide[DbContainer.admin_db]):
    text = msg.text
    if text == MenuOptions.ADMIN_OPTIONS.ADD_LESSON:
        await add_lesson(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.GET_LESSONS:
        await view_lessons(c, msg)
    elif text == MenuOptions.ADMIN_OPTIONS.FIND_USER:
        credentials = (await c.ask(msg.chat.id, "Введіть номер телефону, username або Telegram id")).text
        await retrieve_user_data(c, msg, credentials)
    elif text == MenuOptions.ADMIN_OPTIONS.EXIT:
        admins_db.set_admin_state(str(msg.from_user.id), State.BASE)
        await c.send_message(msg.chat.id, "Ви вийшли з панелі адміна")
        await bot.user.handlers.send_menu(c, msg)
        return

    msg.stop_propagation()


@inject
async def view_lessons(c: Client, msg: Message,
                       lessons_db=Provide[DbContainer.lessons_db]):
    lessons = lessons_db.list()
    s = ""
    for lesson in lessons:
        s += f"{lesson.title} - {lesson.datetime} - {lesson.price}\n{lesson.title} - {lesson.datetime} - {lesson.price}\n"

    await c.send_message(msg.chat.id, s)


@inject
async def add_lesson(c: Client, msg: Message,
                     lessons_db=Provide[DbContainer.lessons_db]):
    chat_id = msg.chat.id
    title = (await c.ask(chat_id, "Введіть назву уроку", filters=filters.private)).text
    while True:
        str_datetime = (await c.ask(chat_id,
                                    "Введіть дату і час проведення у форматі '01.01.2024 10:00'",
                                    filters=filters.private)).text
        if str_datetime == ".":
            break

        try:
            time.strptime(str_datetime, "%d.%m.%Y %H:%M")
            break
        except ValueError:
            log.error(f"Error while parsing datetime from user - {str_datetime}")
            await c.send_message(chat_id, "Невірний формат дати або часу")

    price = (await c.ask(chat_id, "Введіть ціну уроку", filters=filters.private)).text
    description = (await c.ask(chat_id, "Введіть опис уроку", filters=filters.private)).text

    lessons_db.add(LessonDTO(title=title, datetime=str_datetime, price=price, description=description))

    await c.send_message(chat_id, f"Урок доданий - {title}")
    await send_admin_menu(c, msg)


@inject
async def retrieve_user_data(c: Client, msg: Message, credentials: str,
                             clients_db=Provide[DbContainer.clients_db],
                             applies_db=Provide[DbContainer.applies_db],
                             lessons_db=Provide[DbContainer.lessons_db]):
    phone_pattern = r"^\+?3?8?(0-?\d{2}-?\d{3}-?\d{2}-?\d{2})$"
    username_pattern = r"^@\S+$"

    attr = "id"
    if re.match(phone_pattern, credentials):
        attr = "phone_number"
    elif re.match(username_pattern, credentials):
        attr = "username"
        credentials = credentials[1:]

    user = clients_db.get_by_attr(attr, credentials)
    user_assignments = applies_db.get_by_user_id(user.id)
    assigned_lessons: List[LessonDTO] = []
    for ua in user_assignments:
        assigned_lessons.append(lessons_db.get(ua.lesson_id))

    await c.send_message(msg.chat.id,
                         f"**User**:\n\tId: {user.id}\n\t**username**: {user.user_name}\n\t**phone_number**: {user.phone_number}\n\n" +
                         "Assignments:\n" + "\n".join([al.title for al in assigned_lessons]),
                         parse_mode=ParseMode.MARKDOWN)
