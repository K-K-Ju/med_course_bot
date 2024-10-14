from bot.abstract import DTO
from bot.static.states import State, ApplyState
from pyromod import Client


class AdminDTO:
    def __init__(self, _id_, _state_):
        self.id = _id_
        self.state = _state_

    @staticmethod
    def default():
        return AdminDTO(0, 'default')

    @staticmethod
    def from_json(d: dict):
        return AdminDTO(d['id'], d['state'])

    @staticmethod
    def to_json_dict(dto):
        return {
            'id': dto.id,
            'username': dto.state.value
        }


class ClientDTO(DTO):
    def __init__(self, _id_, _username_, _name_, _phone_number_, _state_: State):
        self.id = _id_
        self.user_name = _username_
        self.name = _name_
        self.phone_number = _phone_number_
        self.state = _state_

    @staticmethod
    def default():
        return ClientDTO(0, 'default', '', '', State.NOT_REGISTERED)

    @staticmethod
    def from_json(d: dict):
        return ClientDTO(d['id'], d['username'], d['name'], d['phone_number'],
                         State(int(d['state'])))

    @staticmethod
    def to_json_dict(dto):
        return {
            'id': dto.id,
            'username': dto.user_name,
            'name': dto.name,
            'phone_number': dto.phone_number,
            'state': dto.state.value
        }


class LessonDTO(DTO):
    def __init__(self, _title_, _datetime_, _price_, _description_, _id_=0):
        self.title = _title_
        self.datetime = _datetime_
        self.price = _price_
        self.description = _description_
        self.id = _id_

    @staticmethod
    def default():
        return LessonDTO('default', 'default', 0, '')

    @staticmethod
    def from_json(d):
        ls = LessonDTO(d['title'],
                       d['datetime'],
                       int(d['price']), d['description'], _id_=d['id'])

        return ls

    @staticmethod
    def to_json_dict(dto):
        return {
            'title': dto.title,
            'datetime': dto.datetime,
            'price': dto.price,
            'description': dto.description,
            'id': dto.id
        }


class ApplyDTO(DTO):
    def __init__(self, _user_id_, _lesson_id_, _state_: ApplyState, _id_=0):
        self.user_id = _user_id_
        self.lesson_id = _lesson_id_
        self.state = _state_
        self.id = _id_

    @staticmethod
    def default():
        return ApplyDTO(0, 0, ApplyState.NEW)

    @staticmethod
    def from_json(d: dict):
        return ApplyDTO(int(d['user_id']), d['lesson_id'], ApplyState(d['state']), _id_=d['id'])

    @staticmethod
    def to_json_dict(dto):
        return {
            'user_id': dto.user_id,
            'lesson_id': dto.lesson_id,
            'state': dto.state.value,
            'id': dto.id
        }


class AppClient:
    client: Client = None

    def __init__(self, name, lang, bot_token=None, api_id=None, api_hash=None):
        AppClient.client = Client(name=name, lang_code=lang, bot_token=bot_token, api_id=api_id, api_hash=api_hash)


class Res:
    def __init__(self, _val_):
        self.val = _val_


class Ok(Res):
    pass


class Error(Res):
    pass
