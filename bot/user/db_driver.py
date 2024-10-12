import json
import logging
import redis

from bot.utils import redis_pool
from bot.abstract import AbstractDb
from bot.models import ClientDAO, Error
from bot.static.states import State
from bot.utils import run_query

logger = logging.getLogger('main_logger')


class ClientsDb(AbstractDb):

    def __init__(self):
        logger.info('Connecting to database...')
        self.__r__ = redis.StrictRedis(connection_pool=redis_pool)
        self.__r_json__ = self.__r__.json()
        logger.info('Connection to db established')
    
    def add(self, app_user: ClientDAO):
        logger.debug(f'Adding {app_user.id=}')
        self.__r_json__.arrappend('bot:users', '$.users.clients', ClientDAO.to_json_dict(app_user))
        logger.debug(f'End adding user {app_user.id=}')

    def get(self, user_id) -> ClientDAO:
        logger.debug(f'Retrieving user by {user_id=}')
        res = run_query(lambda: self.__r_json__.get('bot:users', f'$.users.clients[?(@.id=={user_id})]'))

        if res is Error:
            logger.debug('No such user with id=' + user_id)
            return ClientDAO.default()
        else:
            user_json = res.val[0]
            logger.debug(f'End of retrieving user by {user_id=}')
            return ClientDAO.from_json(user_json)

    def get_by_state(self, state: State):
        res = self.__r_json__.get('bot.users', f'$.users.clients[?(@.state={state.value})]')
        clients_json_arr = res.val
        clients = [ClientDAO.from_json(json.loads(c)) for c in clients_json_arr]
        return clients

    def get_faq_section(self, idx):
        res = self.__r__.get(f'faq:{idx}')
        if res is None:
            return res
        else:
            return res.decode('utf-8')

    def set_faq_section(self, idx, section):
        self.__r__.set(f'faq:{idx}', section)

    def remove_faq_section(self, idx):
        self.__r__.delete(f'faq:{idx}')

    def set_state(self, user_id, state: State):
        self.__r_json__.set('bot:users', f'$.users.clients[?(@.id=={user_id})].state', f'"{state.value}"')
    
    def exists(self, user_id):
        logger.debug(f'Checking whether user exists - {user_id}')
        num = self.__r_json__.get('bot:users', f'$.users.clients[?(@.id=={user_id})].id')
        if len(num) == 1:
            return True
        else:
            return False

    def remove(self, idx) -> bool:
        res = self.__r_json__.delete('bot:users', f'$.users.clients[?(@.id=="{idx}")]')
        return res == 1
