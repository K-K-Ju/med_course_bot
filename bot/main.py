from bot.models.app_client import AppClient
from bot.static.enums.commands import BotCommands
from bot.static.regex import APPLY_CALLBACK_HANDLER_INPUT_FORMAT
from logger import prepare_logger

from pyrogram.handlers import CallbackQueryHandler
from pyromod import MessageHandler, Client
from pyrogram import filters

from bot.di import DbContainer, ConfigsContainer
from bot.custom_filters import is_admin, first_is_emoji
from bot.handlers import admin as admin_handlers
from bot.utils import prepare_db
import bot.handlers.client as user_handlers

if __name__ == '__main__':
    configs_container = ConfigsContainer()
    db_container = DbContainer()

    prepare_logger(configs_container.logger_config)

    app_config = configs_container.app_config
    AppClient(name="Med School Bot", lang='ua',
              api_hash=app_config.api_hash,
              api_id=app_config.api_id,
              bot_token=app_config.bot_token)

    prepare_db(db_container.sqlite_con)
    AppClient.handlers = {'user_handler': user_handlers}

    client: Client = AppClient.client

    client.add_handler(MessageHandler(admin_handlers.admin_start,
                                      (filters.command(app_config.admin_key))), group=-1)
    client.add_handler(MessageHandler(admin_handlers.process,
                                      (is_admin() & filters.private & first_is_emoji)))

    client.add_handler(MessageHandler(user_handlers.send_start, (filters.command(BotCommands.start) & filters.private)))
    client.add_handler(MessageHandler(user_handlers.answer, (filters.text & filters.private & first_is_emoji)), group=-1)
    client.add_handler(MessageHandler(user_handlers.send_menu, (filters.command(BotCommands.menu) & filters.private)))
    client.add_handler(MessageHandler(user_handlers.show_status, (filters.command(BotCommands.status) & filters.private)))
    client.add_handler(CallbackQueryHandler(user_handlers.apply,
                                            (filters.regex(APPLY_CALLBACK_HANDLER_INPUT_FORMAT))))

    AppClient.client.run()
