import logging
from typing import NoReturn, List

from bot.db.abstract_db import AbstractDb
from bot.models.dto.client import ClientDTO
from bot.models.res import Ok, Res, Error
from bot.static.enums.states import State
from bot.utils import run_sql

logger = logging.getLogger('main_logger')


class ClientsDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        logger.info('Connecting to database...')
        self._key_path_ = 'clients'
        logger.info('Connection to db established')
    
    def add(self, client: ClientDTO) -> NoReturn:
        logger.debug(f'Adding {client.id=}')
        res = run_sql(self._connection_,
                      lambda: self._connection_.execute(
                          'INSERT INTO clients (id, username, name, phone_number, state)  VALUES (?, ?, ?, ?, ?)',
                          (client.id, client.user_name, client.name, client.phone_number, client.state)
                      ))
        if res is Ok:
            logger.debug(f'Client {client.id} added')
        else:
            logger.error(f'Failed to add client -- {client.id}')

    def get(self, tg_id: str) -> Res[ClientDTO]:
        cur = self._connection_.execute("SELECT * FROM clients WHERE id=?", (tg_id,))
        user_dict = cur.fetchone()
        if user_dict:
            logger.debug(f'Returning client {tg_id}')
            return Ok(ClientDTO.from_dict(user_dict))
        else:
            logger.debug(f'No client with {tg_id=}')
            return Error()

    def get_by_attr(self, attr, value) -> Res[ClientDTO]:
        logger.debug(f'Retrieving user by {attr}={value}')
        cur = self._connection_.execute(f"SELECT * FROM clients WHERE {attr}=?", (value,))
        user_dict = cur.fetchone()
        if user_dict:
            logger.debug(f'Retrieved user by {attr}={value}')
            return ClientDTO.from_dict(user_dict)
        else:
            logger.debug(f'No such user with {attr}={value}')
            return Error()


    def get_by_state(self, state: State) -> List[ClientDTO]:
        cur = self._connection_.execute(
                f"SELECT * FROM clients WHERE state=?", (state,)
        )
        clients = [ClientDTO.from_dict(d) for d in cur]
        return clients

    def set_state(self, user_id, state: State):
        res = run_sql(self._connection_,
                lambda: self._connection_.execute(
                    f"UPDATE clients SET state=? WHERE id=?",(state.value, user_id)
                )
        )
        if res is Ok:
            logger.debug(f'Client {user_id} set state to {state.value}')
        else:
            logger.error(f'Failed to set state -- {user_id}')
    
    def exists(self, idx: str) -> bool:
        logger.debug(f'Checking whether user exists - {idx}')
        cur = self._connection_.execute(f"SELECT id FROM clients WHERE id=?", (idx,))
        user_dict = cur.fetchone()
        if user_dict:
            return True
        return False

    def list(self):
        ...

    def remove(self, idx) -> bool:
        res = self._r_json_.delete(self._key_path_, f'$[?(@.id=="{idx}")]')
        return res == 1

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
