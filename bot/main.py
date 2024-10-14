import logging
import sys

from pyrogram.handlers import CallbackQueryHandler
from pyromod import MessageHandler
from pyrogram import filters

import bot.user.handlers
from logger import prepare_logger
from bot.admin.db_driver import AdminDb
from bot.custom_filters import is_admin, first_is_emoji
from bot.user import handlers as user_handlers
from bot.admin import handlers as admin_handlers
from bot.utils import prepare_db, init_redis_pool
from bot.models import AppClient

import config

config.init_config(sys.argv[1])

prepare_logger(logging.DEBUG, config.config['LOG_FILE_PATH'])
redis_pool = init_redis_pool(config.config['REDIS_HOST'], config.config['REDIS_PORT'])
prepare_db(redis_pool)
bot.user.handlers.inject_dbs(redis_pool)
admin_handlers.inject_dbs(redis_pool)

AppClient(name="Med School Bot", lang='ua')
app = AppClient.client

app.add_handler(MessageHandler(admin_handlers.admin_start,
                               (filters.command(config.config['ADMIN_KEY']))), group=-1)
app.add_handler(MessageHandler(admin_handlers.process,
                               (is_admin(AdminDb(redis_pool)) & filters.private & first_is_emoji)))

app.add_handler(MessageHandler(user_handlers.send_start, (filters.command('start') & filters.private)))
app.add_handler(MessageHandler(user_handlers.answer, (filters.text & filters.private & first_is_emoji)), group=-1)
app.add_handler(MessageHandler(user_handlers.send_menu, (filters.command('menu') & filters.private)))
app.add_handler(MessageHandler(user_handlers.show_status, (filters.command('status'))))
app.add_handler(CallbackQueryHandler(user_handlers.apply,
                                     (filters.regex(
                                         r'{(((\"user_id\":\s\d{9})|(\"lesson_id\":\s\"lesson:\d+\"))(\, )?){2}}'))))

AppClient.client.run()
