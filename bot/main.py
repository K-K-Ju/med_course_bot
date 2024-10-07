import logging
import sys

from pyrogram.handlers import CallbackQueryHandler
from pyromod import MessageHandler
from pyrogram import filters

import bot.admin.db_driver
from bot.utils import prepare_db
from logger import prepare_logger
from bot.models import AppClient

import config
from bot.user import handlers
from bot.admin import handlers as admin_handlers
from bot.custom_filters import is_admin, first_is_emoji

config.init_config(sys.argv[1])

prepare_logger(logging.DEBUG, config.config['LOG_FILE_PATH'])

prepare_db()

AppClient(name="Med School Bot", lang='ua')
app = AppClient.client

app.add_handler(MessageHandler(admin_handlers.admin_start,
                               (filters.regex(config.config['ADMIN_KEY']))), group=-1)
app.add_handler(MessageHandler(admin_handlers.process,
                               (is_admin(bot.admin.db_driver.AdminDb()) & filters.private & first_is_emoji)))

app.add_handler(MessageHandler(handlers.send_start, (filters.command('start') & filters.private)))
app.add_handler(MessageHandler(handlers.answer, (filters.text & filters.private & first_is_emoji)), group=-1)
app.add_handler(MessageHandler(handlers.send_menu, (filters.command('menu') & filters.private)))
app.add_handler(MessageHandler(handlers.show_status, (filters.command('status'))))
app.add_handler(CallbackQueryHandler(handlers.apply,
                                     (filters.regex(r'{(((\"user_id\":\s\d{9})|(\"lesson_id\":\s\"lesson:\d+\"))(\, )?){2}}'))))


AppClient.client.run()
