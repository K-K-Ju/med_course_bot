import json
import logging

from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from pyromod import Client
from pyromod.types import ListenerTypes

from bot.models import AppClient, ApplyDAO
from bot.models import ClientDAO
from bot.static import keyboards
from bot.static.keyboards import (
    MenuOptions,
    ReplyKeyboards
)
from bot.static.messages import Messages
from bot.static.states import State, ApplyState
from bot.user.db_driver import ClientsDb
from bot.db_driver import LessonDb, ApplyDb

logger = logging.getLogger('main_logger')
logger.info('Test logger')
app = AppClient.client
__clients_db__ = ClientsDb()
__lessons_db__ = LessonDb()
__apply_db__ = ApplyDb()


async def send_start(c: Client, msg: Message):
    logger.debug("Received command '/start'")
    await c.send_message(msg.chat.id, Messages.START)
    await send_menu(c, msg)


async def send_menu(c, msg):
    keyboard = ReplyKeyboards.START_NOT_REGISTERED
    if __clients_db__.exists(msg.from_user.id):
        keyboard = ReplyKeyboards.START

    await c.send_message(msg.chat.id,
                         'Оберіть потрібний пункт меню👇',
                         reply_markup=keyboard)


async def show_status(c: Client, msg: Message):
    client = __clients_db__.get(msg.from_user.id)
    applies = __apply_db__.get_by_user_id(msg.from_user.id)
    lessons = []
    for a in applies:
        les = __lessons_db__.get(a.lesson_id)
        lessons.append(les)
    text = f'Name: {client.name}\nApplies:\n\n'
    for i in range(0, len(applies)):
        text += f'{i}. {lessons[i].title} ({lessons[i].datetime})\nstate: {applies[i].state}\n\n'

    await c.send_message(msg.from_user.id, text)


async def register(c: Client, msg: Message):
    user_id = msg.from_user.id
    if __clients_db__.exists(user_id):
        await c.send_message(msg.chat.id, Messages.USE_MENU_REGISTRATION)
        return

    first_name = (await c.ask(msg.chat.id, 'Введіть ваше ім\'я', filters=filters.text)).text
    phone_number = await __get_phone_number__(c, msg)

    app_user = ClientDAO(msg.chat.id,
                         msg.from_user.username, first_name,
                         phone_number, State.BASE)
    __clients_db__.add(app_user)
    logger.debug(f'Registered new user id={user_id}')
    await c.send_message(msg.chat.id, 'Ви успішно зараєструвались! Тепер вам доступно більше функцій😉')
    await send_menu(c, msg)


async def __get_phone_number__(c, msg):
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


async def __send_lessons_list__(c: Client, chat_id):
    lessons = __lessons_db__.get_lessons()
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
    a = ApplyDAO(data['user_id'], data['lesson_id'], ApplyState.NEW)
    success = __apply_db__.add(a)
    if success:
        await c.send_message(data['user_id'], 'Ви записались на урок')
    else:
        logger.error(f'Error while applying - {query.from_user.id=}, {a.lesson_id=}')
        await c.send_message(data['user_id'], 'Виникла помилка. Спробуйте пізніше або зв\'яжіться з менеджером')


async def show_faq(c: Client, msg: Message):
    chat_id = msg.chat.id
    msg = await c.ask(chat_id, 'Choose section', reply_markup=ReplyKeyboards.FAQ)
    while True:
        sec = __clients_db__.get_faq_section(chat_id)

        if msg.text == MenuOptions.BACK:
            if sec is None:
                await send_menu(c, msg)
                break
            __clients_db__.remove_faq_section(chat_id)
            msg = await c.ask(chat_id, 'Choose option', reply_markup=ReplyKeyboards.FAQ)
            continue

        if sec is None:
            reply_keyboard = keyboards.faq_mapping[msg.text]['keyboard']
            __clients_db__.set_faq_section(chat_id, msg.text)
            msg = await c.ask(chat_id, 'Choose option', reply_markup=reply_keyboard)
        else:
            faq_info = keyboards.faq_mapping[sec][msg.text]
            msg = await c.ask(chat_id, faq_info)


async def answer(c, msg: Message):
    chat_id = msg.chat.id
    if msg.text == MenuOptions.START_MENU.STATUS:
        await show_status(c, msg)
    elif msg.text == MenuOptions.START_MENU.APPLY:
        await __send_lessons_list__(c, msg.chat.id)
    elif msg.text == MenuOptions.START_MENU.FAQ:
        await show_faq(c, msg)
    elif msg.text == MenuOptions.START_MENU.REGISTER:
        await register(c, msg)
    elif msg.text == MenuOptions.START_MENU.CONTACT_MANAGER:
        await c.send_message(chat_id, 'Перейдіть до бота підтримки <a href="https://t.me/med_school_support_bot">посилання</a>')
    elif msg.text == MenuOptions.START_MENU.MENU:
        await send_menu(c, msg)
