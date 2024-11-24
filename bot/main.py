import logging
from config import app_config
from logger import prepare_logger

from pyrogram.handlers import CallbackQueryHandler
from pyromod import MessageHandler, Client
from pyrogram import filters

from bot.di import DbContainer
from bot.admin.db_driver import AdminDb
from bot.custom_filters import is_admin, first_is_emoji
from bot.admin import handlers as admin_handlers
from bot.utils import prepare_db, init_redis_pool
from bot.models import AppClient
import bot.user.handlers as user_handlers

if __name__ == '__main__':
    prepare_logger(logging.DEBUG, app_config.log_file_path)
    redis_pool = init_redis_pool(app_config.redis_host, app_config.redis_port)
    prepare_db(redis_pool)
    db_container = DbContainer()
    db_container.wire()
    AppClient(name="Med School Bot", lang='ua',
              api_hash=app_config.api_hash,
              api_id=app_config.api_id,
              bot_token=app_config.bot_token)

    AppClient.handlers = {'user_handler': user_handlers}
    client: Client = AppClient.client



    client.add_handler(MessageHandler(admin_handlers.admin_start,
                                      (filters.command(app_config.admin_key))), group=-1)
    client.add_handler(MessageHandler(admin_handlers.process,
                                      (is_admin(AdminDb(redis_pool)) & filters.private & first_is_emoji)))

    client.add_handler(MessageHandler(user_handlers.send_start, (filters.command('start') & filters.private)))
    client.add_handler(MessageHandler(user_handlers.answer, (filters.text & filters.private & first_is_emoji)), group=-1)
    client.add_handler(MessageHandler(user_handlers.send_menu, (filters.command('menu') & filters.private)))
    client.add_handler(MessageHandler(user_handlers.show_status, (filters.command('status'))))
    client.add_handler(CallbackQueryHandler(user_handlers.apply,
                                            (filters.regex(
                                             r'{(((\"user_id\":\s\d{9})|(\"lesson_id\":\s\"lesson:\d+\"))(\, )?){2}}'))))

    AppClient.client.run()
