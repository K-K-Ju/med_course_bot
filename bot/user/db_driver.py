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
        self.r = redis.Redis(connection_pool=_connection_pool_)
        self.__r_json__ = self.r.json()
        logger.info('Connection to db established')
    
    def add(self, app_user: ClientDTO):
        logger.debug(f'Adding {app_user.id=}')
        self.__r_json__.arrappend('bot:users:clients', '$', ClientDTO.to_json_dict(app_user))
        logger.debug(f'End adding user {app_user.id=}')

    def get(self, user_id) -> ClientDTO:
        logger.debug(f'Retrieving user by {user_id=}')
        res = run_query(lambda: self.__r_json__.get('bot:users:clients', f'$[?(@.id=={user_id})]'))

        if res is Error:
            logger.debug('No such user with id=' + user_id)
            return ClientDTO.default()
        else:
            user_json = res.val[0]
            logger.debug(f'End of retrieving user by {user_id=}')
            return ClientDTO.from_json(user_json)

    def get_by_state(self, state: State):
        res = self.__r_json__.get('bot:users:clients', f'$[?(@.state={state.value})]')
        clients_json_arr = res.val
        clients = [ClientDTO.from_json(json.loads(c)) for c in clients_json_arr]
        return clients

    def get_faq_section(self, idx):
        res = self.r.get(f'faq:{idx}')
        if res is None:
            return res
        else:
            return res.decode('utf-8')

    def set_faq_section(self, idx, section):
        self.r.set(f'faq:{idx}', section)

    def remove_faq_section(self, idx):
        self.r.delete(f'faq:{idx}')

    def set_state(self, user_id, state: State):
        self.__r_json__.set('bot:users:clients', f'$[?(@.id=={user_id})].state', f'"{state.value}"')
    
    def exists(self, user_id):
        logger.debug(f'Checking whether user exists - {user_id}')
        num = self.__r_json__.get('bot:users:clients', f'$[?(@.id=={user_id})].id')
        if num and len(num) == 1:
            return True
        else:
            return False

    def remove(self, idx) -> bool:
        res = self.__r_json__.delete('bot:users:clients', f'$[?(@.id=="{idx}")]')
        return res == 1
