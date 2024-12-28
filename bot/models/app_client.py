from pyromod import Client
from typing import Dict

from bot.db.abstract_db import Handler


class AppClient:
    client: Client = None
    handlers: Dict[str, Handler] = {}
    def __init__(self, name, lang, bot_token=None, api_id=None, api_hash=None):
        AppClient.client = Client(name=name, lang_code=lang, bot_token=bot_token, api_id=api_id, api_hash=api_hash)