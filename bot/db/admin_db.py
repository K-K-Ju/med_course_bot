import logging

from bot.db.abstract_db import AbstractDb, DTO
from bot.models.dto.admin import AdminDTO
from bot.models.res import Ok
from bot.static.enums.states import State
from bot.utils import run_sql

logger = logging.getLogger('main_logger')


class AdminDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        logger.info('Preparing admin db driver...')
        self._table_ = 'admins'
        logger.info('Admin db preparing is finished')

    def add(self, admin_dto: AdminDTO):
        logger.info(f'Adding admin with {admin_dto.id=}')
        res = run_sql(self._connection_,
                      lambda: self._connection_.execute(
                          'INSERT INTO admins (client_id, state) VALUES (?, ?)',
                          (admin_dto.id, admin_dto.state))
                      )
        if res is Ok:
            logger.debug(f'New admin added {admin_dto.id=}')
        else:
            logger.error(f'Failed to add admin {admin_dto.id=}')

    def is_admin(self, user_id: str) -> bool:
        logger.debug(f'Checking whether {user_id} is admin')
        cur = self._connection_.execute('SELECT client_id FROM admins WHERE client_id=?', (user_id,))
        if cur.fetchone():
            return True
        return False

    def get_state(self, user_id: str) -> State:
        cur = self._connection_.execute(
            'SELECT state FROM admins WHERE client_id=?', (user_id,)
        )
        d = cur.fetchone()
        if d:
            return State(d['state'])
        else:
            return State.NOT_REGISTERED

    def set_admin_state(self, user_id: str, state: State):
        res = run_sql(self._connection_,
                      lambda: self._connection_.execute(
                          'UPDATE admins SET state=? WHERE client_id=?',
                          (state.value, user_id))
                      )
        if res is Ok:
            logger.info(f'Admin {user_id} set state to {state.value}')
        else:
            logger.info(f'Failed to set admin {user_id} state to {state.value}')

    def list(self):
        ...

    def remove(self, user_id):
        ...

    def get(self, idx) -> DTO:
        ...
