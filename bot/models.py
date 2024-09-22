from bot.static.states import State, ApplyState
from pyromod import Client


class DAO:

    @staticmethod
    def default():
        pass

    @staticmethod
    def from_json(d: dict):
        TypeError()

    @staticmethod
    def to_json_dict(dao):
        TypeError()


class ClientDAO(DAO):
    def __init__(self, _id_, _username_, _name_, _phone_number_, _state_: State):
        self.id = _id_
        self.user_name = _username_
        self.name = _name_
        self.phone_number = _phone_number_
        self.state = _state_

    @staticmethod
    def default():
        return ClientDAO(0, 'default', '', '', State.NOT_REGISTERED)

    @staticmethod
    def from_json(d: dict):
        return ClientDAO(d['id'], d['username'], d['name'], d['phone_number'],
                         State(int(d['state'])))

    @staticmethod
    def to_json_dict(dao):
        return {
            'id': dao.id,
            'username': dao.user_name,
            'name': dao.name,
            'phone_number': dao.phone_number,
            'state': dao.state.value
        }


class LessonDAO(DAO):
    def __init__(self, _title_, _datetime_, _price_, _description_, _id_=0):
        self.title = _title_
        self.datetime = _datetime_
        self.price = _price_
        self.description = _description_
        self.id = _id_

    @staticmethod
    def default():
        return LessonDAO('default', 'default', 0, '')

    @staticmethod
    def from_json(d):
        ls = LessonDAO(d['title'],
                       d['datetime'],
                       int(d['price']), d['description'], _id_=d['id'])

        return ls

    @staticmethod
    def to_json_dict(dao):
        return {
            'title': dao.title,
            'datetime': dao.datetime,
            'price': dao.price,
            'description': dao.description,
            'id': dao.id
        }


class ApplyDAO(DAO):
    def __init__(self, _user_id_, _lesson_id_, _state_: ApplyState, _id_=0):
        self.user_id = _user_id_
        self.lesson_id = _lesson_id_
        self.state = _state_
        self.id = _id_

    @staticmethod
    def default():
        return ApplyDAO(0, 0, ApplyState.NEW)

    @staticmethod
    def from_json(d: dict):
        return ApplyDAO(int(d['user_id']), int(d['lesson_id']), ApplyState(d['state']), _id_=d['id'])

    @staticmethod
    def to_json_dict(dao):
        return {
            'user_id': dao.user_id,
            'lesson_id': dao.lesson_id,
            'state': dao.state.value,
            'id': dao.id
        }


class AppClient:
    client: Client = None

    def __init__(self, name, lang):
        AppClient.client = Client(name=name, lang_code=lang)


class Res:
    def __init__(self, _val_):
        self.val = _val_


class Ok(Res):
    pass


class Error(Res):
    pass
