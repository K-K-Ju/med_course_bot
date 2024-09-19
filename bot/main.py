import logging

import redis
from pyrogram.handlers import CallbackQueryHandler
from pyromod import MessageHandler
from pyrogram import filters

import bot.admin.db_driver
from bot import redis_pool
from logger import prepare_logger
from bot.models import AppClient

import config
from bot.user import handlers
from bot.admin import handlers as admin_handlers
from bot.custom_filters import is_admin, first_is_emoji

config.init_config('C:\\Users\\tusen\\Developing\\Python\\med_course_bot\\secrets.json')

prepare_logger(logging.DEBUG, config.config['LOG_FILE_PATH'])


def prepare_db():
    r = redis.Redis(connection_pool=redis_pool)
    docs = {'bot:users': '{"users":{"clients":[], "admins":[]}}',
            'bot:lessons': '{"lessons":[]}',
            'bot:applies': '{"applies": []}'}

    for doc_name, doc_struct in docs.items():
        res = r.json().get(doc_name, '$')
        if not res:
            r.json().set(doc_name, '$', doc_struct)

    print('Testing database...')
    test_key, test_value = 'test_key', 100
    r.set(test_key, format(test_value, 'b'))
    res = int(r.get(test_key), 2)
    assert res == test_value
    r.delete(test_key)
    print('Finished testing database')


prepare_db()

AppClient(name="Surgeon Course Bot", lang='ua')
app = AppClient.client

app.add_handler(MessageHandler(admin_handlers.admin_start,
                               (filters.regex(config.config['ADMIN_KEY']))), group=-1)
app.add_handler(MessageHandler(admin_handlers.process,
                               (is_admin(bot.admin.db_driver.AdminDb()) & filters.text & filters.private & first_is_emoji)))

app.add_handler(MessageHandler(handlers.send_start, (filters.command('start') & filters.private)))
app.add_handler(MessageHandler(handlers.answer, (filters.text & filters.private & first_is_emoji)), group=-1)
app.add_handler(MessageHandler(handlers.send_menu, (filters.command('menu') & filters.private)))
app.add_handler(MessageHandler(handlers.show_status, (filters.command('status'))))
app.add_handler(CallbackQueryHandler(handlers.apply, (filters.private & filters.regex('id=[0-9]+'))))


AppClient.client.run()
