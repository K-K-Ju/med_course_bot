from bot.static.states import State
from pyromod import Client


class AppUser:
    def __init__(self, _user_id_, _chat_id_, _username_, _name_, _phone_number_, _state_: State):
        self.user_id = _user_id_
        self.chat_id = _chat_id_
        self.user_name = _username_
        self.name = _name_
        self.phone_number = _phone_number_
        self.state = _state_

    @staticmethod
    def from_redis_dict(d: dict):
        AppUser(d['user_id'], d['chat_id'], d['username'], d['name'], d['phone_number'], State(int(d['state'], 2)))


class AppClient:
    client = None

    def __init__(self, name, lang):
        AppClient.client = Client(name=name, lang_code=lang)
