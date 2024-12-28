import json
import logging

from dependency_injector.wiring import inject, Provide
from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from pyromod import Client
from pyromod.types import ListenerTypes

import bot.handlers.admin
from bot.di import DbContainer
from bot.models.app_client import AppClient
from bot.models.dto.apply import ApplyDTO
from bot.models.dto.client import ClientDTO
from bot.static import keyboards
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.enums.states import State, APPLY_STATE_TEXT_MAPPING

logger = logging.getLogger("main_logger")
app = AppClient.client


async def send_start(c: Client, msg: Message):
    logger.debug("Received command '/start'")
    await c.send_message(msg.chat.id, Messages.START)
    await send_menu(c, msg)


@inject
async def send_menu(c: Client, msg: Message,
                    clients_db=Provide[DbContainer.clients_db],
                    admins_db=Provide[DbContainer.admin_db]):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    # TODO caching
    if clients_db.exists(str(msg.from_user.id)):
        keyboard = ReplyKeyboards.START
        if admins_db.is_admin(str(msg.from_user.id)):
            keyboard = ReplyKeyboards.ADMIN_USER_START

    await c.send_message(msg.chat.id,
                         "Оберіть потрібний пункт меню👇",
                         reply_markup=keyboard)


@inject
async def show_status(c: Client, msg: Message,
                      clients_db=Provide[DbContainer.clients_db],
                      applies_db=Provide[DbContainer.applies_db],
                      lessons_db=Provide[DbContainer.lessons_db]):
    client = clients_db.get(str(msg.from_user.id))
    applies = applies_db.get_by_user_id(str(msg.from_user.id))
    lessons = []
    for a in applies:
        les = lessons_db.get(a.lesson_id)
        lessons.append(les)
    text = f"**Ім\"я**: {client.name}\n**Записи**:\n\n"
    for i in range(0, len(applies)):
        text += f"{i}. {lessons[i].title} ({lessons[i].datetime})\nстан: {APPLY_STATE_TEXT_MAPPING[applies[i].state.value]}\n"

    await c.send_message(msg.from_user.id, text)


@inject
async def register(c: Client, msg: Message,
                   clients_db=Provide[DbContainer.clients_db]):
    user_id = msg.from_user.id
    if clients_db.exists(str(user_id)):
        await c.send_message(msg.chat.id, Messages.USE_MENU_REGISTRATION)
        return

    first_name = (await c.ask(msg.chat.id, "Введіть ваше ім\"я", filters=filters.text)).text
    phone_number = await _get_phone_number_(c, msg)

    app_user = ClientDTO(idx=str(msg.chat.id),
                         username=msg.from_user.username,
                         name=first_name,
                         phone_number=phone_number,
                         state=State.BASE)

    clients_db.add(app_user)
    logger.debug(f"Registered new user id={user_id}")
    await c.send_message(msg.chat.id, "Ви успішно зараєструвались! Тепер вам доступно більше функцій😉")
    await send_menu(c, msg)


async def _get_phone_number_(c: Client, msg: Message):
    if msg.contact:
        return msg.contact.phone_number
    else:
        await msg.reply(
            text="Дозвольте прочитати ваш номер телефону👉👈",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Поділитись", request_contact=True)],
                ],
                resize_keyboard=True,
            ),
        )
        contact_msg = await c.listen(chat_id=msg.chat.id, filters=filters.contact,
                                     listener_type=ListenerTypes.MESSAGE)
        return contact_msg.contact.phone_number


@inject
async def _send_lessons_list_(c: Client, chat_id,
                              lessons_db=Provide[DbContainer.lessons_db]):
    lessons = lessons_db.list()
    # TODO filtration
    for l in lessons:
        data = {"user_id": chat_id, "lesson_id": l.id}
        data_json = json.dumps(data)
        await c.send_message(chat_id, f"Title - {l.title}\nPrice - {l.description}",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton("Записатись", callback_data=data_json)]
                             ]))


@inject
async def apply(c: Client, query: CallbackQuery,
                applies_db=Provide[DbContainer.applies_db]):
    data = json.loads(query.data)
    a = ApplyDTO.model_validate_json(data)
    success = applies_db.add(a)
    if success:
        await c.send_message(data["user_id"], "Ви записались на урок")
        await query.answer()
    else:
        logger.error(f"Error while applying - {query.from_user.id=}, {a.lesson_id=}")
        await c.send_message(data["user_id"], "Виникла помилка. Спробуйте пізніше або зв\"яжіться з менеджером")
        await query.answer()


@inject
async def show_faq(c: Client, msg: Message,
                   clients_db=Provide[DbContainer.clients_db]):
    chat_id = msg.chat.id
    msg = await c.ask(chat_id, "Choose section", reply_markup=ReplyKeyboards.FAQ)
    while True:
        sec = clients_db.get_faq_section(chat_id)

        if msg.text == MenuOptions.BACK:
            if sec is None:
                await send_menu(c, msg)
                break
            clients_db.remove_faq_section(chat_id)
            msg = await c.ask(chat_id, "Choose option", reply_markup=ReplyKeyboards.FAQ)
            continue

        if sec is None:
            reply_keyboard = keyboards.faq_mapping[msg.text]["keyboard"]
            clients_db.set_faq_section(chat_id, msg.text)
            msg = await c.ask(chat_id, "Choose option", reply_markup=reply_keyboard)
        else:
            faq_info = keyboards.faq_mapping[sec][msg.text]
            msg = await c.ask(chat_id, faq_info)


async def receive_recipe(c: Client, msg: Message):
    ...


async def answer(c: Client, msg: Message):
    chat_id = str(msg.chat.id)
    if msg.text == MenuOptions.START_MENU.STATUS:
        await show_status(c, msg)
    elif msg.text == MenuOptions.START_MENU.APPLY:
        await _send_lessons_list_(c, msg.chat.id)
    elif msg.text == MenuOptions.START_MENU.FAQ:
        await show_faq(c, msg)
    elif msg.text == MenuOptions.START_MENU.REGISTER:
        await register(c, msg)
    elif msg.text == MenuOptions.START_MENU.CONTACT_MANAGER:
        await c.send_message(chat_id,
                             'Перейдіть до бота підтримки <a href="https://t.me/med_school_support_bot">посилання</a>')
    elif msg.text == MenuOptions.START_MENU.MENU:
        await send_menu(c, msg)
    elif msg.text == MenuOptions.START_MENU.SEND_RECIPE:
        if msg.document:
            await receive_recipe(c, msg)
    elif msg.text == MenuOptions.ADMIN_PANEL:
        await bot.handlers.handlers.admin_start(c, msg)
