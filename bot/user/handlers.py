import json
import logging

from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from pyromod import Client
from pyromod.types import ListenerTypes

import bot.admin.handlers
from bot.di import DbContainer
from bot.models import AppClient, ApplyDTO
from bot.models import ClientDTO
from bot.static import keyboards
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.states import State, ApplyState, APPLY_STATE_TEXT_MAPPING

logger = logging.getLogger('main_logger')
app = AppClient.client

_clients_db_ = DbContainer.clients_db()
_lessons_db_ = DbContainer.lessons_db()
_applies_db_ = DbContainer.applies_db()
_admin_db_ = DbContainer.admin_db()


async def send_start(c: Client, msg: Message):
    logger.debug("Received command '/start'")
    await c.send_message(msg.chat.id, Messages.START)
    await send_menu(c, msg)


async def send_menu(c: Client, msg: Message):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    # TODO caching
    if _clients_db_.exists(str(msg.from_user.id)):
        keyboard = ReplyKeyboards.START
        if _admin_db_.is_admin(str(msg.from_user.id)):
            keyboard = ReplyKeyboards.ADMIN_USER_START

    await c.send_message(msg.chat.id,
                         'Оберіть потрібний пункт меню👇',
                         reply_markup=keyboard)


async def show_status(c: Client, msg: Message):
    client = _clients_db_.get(str(msg.from_user.id))
    applies = _applies_db_.get_by_user_id(str(msg.from_user.id))
    lessons = []
    for a in applies:
        les = _lessons_db_.get(a.lesson_id)
        lessons.append(les)
    text = f'**Ім\'я**: {client.name}\n**Записи**:\n\n'
    for i in range(0, len(applies)):
        text += f'{i}. {lessons[i].title} ({lessons[i].datetime})\nстан: {APPLY_STATE_TEXT_MAPPING[applies[i].state.value]}\n'

    await c.send_message(msg.from_user.id, text)


async def register(c: Client, msg: Message):
    user_id = msg.from_user.id
    if _clients_db_.exists(str(user_id)):
        await c.send_message(msg.chat.id, Messages.USE_MENU_REGISTRATION)
        return

    first_name = (await c.ask(msg.chat.id, 'Введіть ваше ім\'я', filters=filters.text)).text
    phone_number = await _get_phone_number_(c, msg)

    app_user = ClientDTO(str(msg.chat.id),
                         msg.from_user.username, first_name,
                         phone_number, State.BASE)
    _clients_db_.add(app_user)
    logger.debug(f'Registered new user id={user_id}')
    await c.send_message(msg.chat.id, 'Ви успішно зараєструвались! Тепер вам доступно більше функцій😉')
    await send_menu(c, msg)


async def _get_phone_number_(c: Client, msg: Message):
    if msg.contact:
        return msg.contact.phone_number
    else:
        await msg.reply(
            text='Дозвольте прочитати ваш номер телефону👉👈',
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Поділитись', request_contact=True)],
                ],
                resize_keyboard=True,
            ),
        )
        contact_msg = await c.listen(chat_id=msg.chat.id, filters=filters.contact,
                                     listener_type=ListenerTypes.MESSAGE)
        return contact_msg.contact.phone_number


async def _send_lessons_list_(c: Client, chat_id):
    lessons = _lessons_db_.list()
    # TODO filtration
    for l in lessons:
        data = {'user_id': chat_id, 'lesson_id': l.id}
        data_json = json.dumps(data)
        await c.send_message(chat_id, f'Title - {l.title}\nPrice - {l.description}',
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton('Записатись', callback_data=data_json)]
                             ]))


async def apply(c: Client, query: CallbackQuery):
    data = json.loads(query.data)
    a = ApplyDTO(data['user_id'], data['lesson_id'], ApplyState.NEW)
    success = _applies_db_.add(a)
    if success:
        await c.send_message(data['user_id'], 'Ви записались на урок')
        await query.answer()
    else:
        logger.error(f'Error while applying - {query.from_user.id=}, {a.lesson_id=}')
        await c.send_message(data['user_id'], 'Виникла помилка. Спробуйте пізніше або зв\'яжіться з менеджером')
        await query.answer()


async def show_faq(c: Client, msg: Message):
    chat_id = msg.chat.id
    msg = await c.ask(chat_id, 'Choose section', reply_markup=ReplyKeyboards.FAQ)
    while True:
        sec = _clients_db_.get_faq_section(chat_id)

        if msg.text == MenuOptions.BACK:
            if sec is None:
                await send_menu(c, msg)
                break
            _clients_db_.remove_faq_section(chat_id)
            msg = await c.ask(chat_id, 'Choose option', reply_markup=ReplyKeyboards.FAQ)
            continue

        if sec is None:
            reply_keyboard = keyboards.faq_mapping[msg.text]['keyboard']
            _clients_db_.set_faq_section(chat_id, msg.text)
            msg = await c.ask(chat_id, 'Choose option', reply_markup=reply_keyboard)
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
        await bot.admin.handlers.admin_start(c, msg)
