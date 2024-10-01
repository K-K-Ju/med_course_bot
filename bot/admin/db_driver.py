import logging

import redis

from bot.utils import redis_pool
from bot.static.states import State

logger = logging.getLogger('main_logger')


class AdminDb:
    def __init__(self, _connection_pool_=redis_pool):
        logger.info('Preparing admin db driver...')
        self.__r__ = redis.StrictRedis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        logger.info('Admin db preparing is finished')

    def is_admin(self, user_id):
        logger.debug(f'Checking whether {user_id} is admin')
        res = self.__r_json__.get('bot:users', f'$.users.admins[?(@.id=={user_id})].id')

        if len(res) == 1:
            return True
        else:
            return False

    def get_state(self, user_id) -> State:
        res = self.__r_json__.get('bot:users', f'$.users.admins[?(@.id=={user_id})].state')
        if len(res) == 1:
            return State(res[0])
        else:
            return State.NOT_REGISTERED

    def set_admin_state(self, user_id, state: State):
        self.__r_json__.set('bot:users', f'$.users.admins[?(@.id=={user_id})].state', state.value)
