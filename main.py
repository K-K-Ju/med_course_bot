from pyrogram import Client, filters
from pyrogram.enums import ChatType

import logging
import db_driver
import messages
import logger

logger.prepare_logger(logging.INFO)
logger = logging.getLogger('main_logger')

logger.info('Test logger')
app = Client("Surgeon Course Bot", lang_code='ua')
db_driver.prepare_db()


@app.on_message(filters.command('start') & filters.private)
async def send_start(client: Client, message):
    logger.debug("Received command '/start'")
    if message.chat.type == ChatType.PRIVATE:
        user = message.from_user
        user_id, username = user.id, user.username
        if not db_driver.user_exists(user_id):
            db_driver.add_client(user_id, username, message.chat.id)
            logger.debug(f"Added new {username=}")

    await client.send_message(message.chat.id,
                              messages.START)


app.run()
