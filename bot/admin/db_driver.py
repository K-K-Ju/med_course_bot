import logging

import redis

from bot.abstract import AbstractDb, DTO
from bot.models import AdminDTO
from bot.static.states import State

logger = logging.getLogger('main_logger')


class AdminDb(AbstractDb):
    def __init__(self, connection_pool):
        super().__init__(connection_pool)
        logger.info('Preparing admin db driver...')
        self._key_path_ = 'bot:users:admins'
        logger.info('Admin db preparing is finished')

    def add(self, admin_dto: AdminDTO):
        logger.info(f'Adding admin with {admin_dto.id=}')
        res = self._r_json_.arrappend(self._key_path_, '$', AdminDTO.to_json_dict(admin_dto))
        if res:
            logger.info(f'New admin added {admin_dto.id=}')
        else:
            logger.info(f'Failed to add admin {admin_dto.id=}')

    def is_admin(self, user_id: str):
        logger.debug(f'Checking whether {user_id} is admin')
        res = self._r_json_.get(self._key_path_, f'$[?(@.id=="{user_id}")].id')

        if res and len(res) == 1:
            return True
        else:
            return False

    def get_state(self, user_id: str) -> State:
        res = self._r_json_.get(self._key_path_, f'$[?(@.id=="{user_id}")].state')
        if res and len(res) == 1:
            return State(res[0])
        else:
            return State.NOT_REGISTERED

    def set_admin_state(self, user_id: str, state: State):
        self._r_json_.set(self._key_path_, f'$[?(@.id=="{user_id}")].state', state.value)

    def list(self):
        ...

    def remove(self, user_id):
        ...

    def get(self, idx) -> DTO:
        ...