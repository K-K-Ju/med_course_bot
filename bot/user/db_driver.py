import json
import logging
import redis
from bot.abstract import AbstractDb
from bot.models import ClientDTO, Error
from bot.static.states import State
from bot.utils import run_query

logger = logging.getLogger('main_logger')


class ClientsDb(AbstractDb):
    def __init__(self, _connection_pool_):
        logger.info('Connecting to database...')
        self._key_path_ = 'bot:users:clients'
        self._r_ = redis.Redis(connection_pool=_connection_pool_)
        self._r_json_ = self._r_.json()
        logger.info('Connection to db established')
    
    def add(self, app_user: ClientDTO):
        logger.debug(f'Adding {app_user.id=}')
        self._r_json_.arrappend(self._key_path_, '$', ClientDTO.to_json_dict(app_user))
        logger.debug(f'End adding user {app_user.id=}')

    def get(self, tg_id: str) -> ClientDTO:
        logger.debug(f'Getting {tg_id=}')
        res = run_query(lambda: self._r_json_.get(self._key_path_, f'$[?(@.id=="{tg_id}")]'))
        if res is Error:
            logger.debug(f'No such user with {tg_id=}')
            return ClientDTO.default()
        else:
            user_json = res.val[0]
            logger.debug(f'End of retrieving user by {tg_id=}')
            return ClientDTO.from_json(user_json)

    def get_by_attr(self, attr, value) -> ClientDTO:
        logger.debug(f'Retrieving user by {attr}={value}')
        res = run_query(lambda: self._r_json_.get(self._key_path_, f"$[?(@.{attr}=='{value}')]"))

        if res is Error:
            logger.debug(f'No such user with {attr}={value}')
            return ClientDTO.default()
        else:
            user_json = res.val[0]
            logger.debug(f'End of retrieving user by {attr}={value}')
            return ClientDTO.from_json(user_json)


    def get_by_state(self, state: State):
        res = self._r_json_.get(self._key_path_, f'$[?(@.state={state.value})]')
        clients_json_arr = res.val
        clients = [ClientDTO.from_json(json.loads(c)) for c in clients_json_arr]
        return clients

    def get_faq_section(self, idx):
        res = self._r_.get(f'faq:{idx}')
        if res is None:
            return res
        else:
            return res.decode('utf-8')

    def set_faq_section(self, idx, section):
        self._r_.set(f'faq:{idx}', section)

    def remove_faq_section(self, idx):
        self._r_.delete(f'faq:{idx}')

    def set_state(self, user_id, state: State):
        self._r_json_.set(self._key_path_, f'$[?(@.id=="{user_id}")].state', f'"{state.value}"')
    
    def exists(self, user_id: str):
        logger.debug(f'Checking whether user exists - {user_id}')
        num = self._r_json_.get(self._key_path_, f'$[?(@.id=="{user_id}")].id')
        if num and len(num) == 1:
            return True
        else:
            return False

    def remove(self, idx) -> bool:
        res = self._r_json_.delete(self._key_path_, f'$[?(@.id=="{idx}")]')
        return res == 1

    def list(self):
        ...
