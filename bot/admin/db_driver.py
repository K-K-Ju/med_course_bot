import logging

import redis

from bot.models import AdminDTO
from bot.static.states import State

logger = logging.getLogger('main_logger')


class AdminDb:
    def __init__(self, _connection_pool_):
        logger.info('Preparing admin db driver...')
        self.__r__ = redis.StrictRedis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        logger.info('Admin db preparing is finished')

    def add(self, admin_dto: AdminDTO):
        logger.info(f'Adding admin with {admin_dto.id=}')
        res = self.__r_json__.arrappend('bot:users:admins', '$', AdminDTO.to_json_dict(admin_dto))
        if res:
            logger.info(f'New admin added {admin_dto.id=}')
        else:
            logger.info(f'Failed to add admin {admin_dto.id=}')

    def is_admin(self, user_id):
        logger.debug(f'Checking whether {user_id} is admin')
        res = self.__r_json__.get('bot:users:admins', f'$[?(@.id=={user_id})].id')

        if res and len(res) == 1:
            return True
        else:
            return False

    def get_state(self, user_id) -> State:
        res = self.__r_json__.get('bot:users:admins', f'$[?(@.id=={user_id})].state')
        if res and len(res) == 1:
            return State(res[0])
        else:
            return State.NOT_REGISTERED

    def set_admin_state(self, user_id, state: State):
        self.__r_json__.set('bot:users:admins', f'$[?(@.id=={user_id})].state', state.value)
