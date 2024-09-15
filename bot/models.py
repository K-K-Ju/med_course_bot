from redis.commands.search.field import TextField, TagField, NumericField

from bot.static.states import State
from pyromod import Client


class DAO:
    @staticmethod
    def from_redis_dict(d: dict):
        TypeError()


class AppUserDAO(DAO):
    schema = (
        TextField("$.chat_id", as_name="name"),
        TextField("$.username", as_name="username"),
        TextField("$.phone_number", as_name="phone_number"),
        NumericField("$.state", as_name="state")
    )

    def __init__(self, _user_id_, _chat_id_, _username_, _name_, _phone_number_, _state_: State):
        self.user_id = _user_id_
        self.chat_id = _chat_id_
        self.user_name = _username_
        self.name = _name_
        self.phone_number = _phone_number_
        self.state = _state_

    @staticmethod
    def from_redis_dict(d: dict):
        return AppUserDAO(d[b'user_id'], d[b'chat_id'], d[b'username'], d[b'name'], d[b'phone_number'],
                          State(int(d[b'state'].decode('utf-8'))))


class LessonDAO(DAO):
    schema = (
        TextField("$.title", as_name="title"),
        TextField("$.date", as_name="date"),
        TextField("$.time", as_name="time"),
        NumericField("$.price", as_name="price"),
        TextField("$.description", as_name="description"),
    )

    def __init__(self, _title_, _datetime_, _price_, _description_, **kwargs):
        self.title = _title_
        self.datetime = _datetime_
        self.price = _price_
        self.description = _description_
        self.id = kwargs['_id_']

    @staticmethod
    def from_redis_dict(d: dict):
        ls = LessonDAO(d[b'title'].decode('utf-8'),
                       d[b'datetime'].decode('utf-8'),
                       int(d[b'price'].decode('utf-8')), d[b'description'].decode('utf-8'), _id_=d['id'])

        return ls


class AppClient:
    client: Client = None

    def __init__(self, name, lang):
        AppClient.client = Client(name=name, lang_code=lang)
