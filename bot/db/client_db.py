import logging
from typing import NoReturn, List, Optional

from bot.db.abstract_db import AbstractDb
from bot.models.dto.client import ClientDTO
from bot.models.res import Ok
from bot.static.enums.states import State
from bot.utils import run_sql, get_single_dict_by_sql

logger = logging.getLogger('main_logger')


class ClientsDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        logger.info('Connecting to database...')
        self._key_path_ = 'clients'
        logger.info('Connection to db established')

    def add(self, client: ClientDTO) -> NoReturn:
        logger.debug(f'Adding {client.id=}')
        res = run_sql(self._connection,
                      lambda: self._connection.execute(
                          'INSERT INTO clients (id, username, name, phone_number, state)  VALUES (?, ?, ?, ?, ?)',
                          (client.id, client.user_name, client.name, client.phone_number, client.state)
                      ))
        if res is Ok:
            logger.debug(f'Client {client.id} added')
        else:
            logger.error(f'Failed to add client -- {client.id}')

    def get(self, tg_id: str) -> Optional[ClientDTO]:
        client_dict = get_single_dict_by_sql(
            self._connection,
            lambda: self._connection.execute("SELECT * FROM clients WHERE id=?", (tg_id,))
        )

        if client_dict is None:
            logger.debug(f'Error occurred while getting client with {tg_id=}')
            return None

        logger.debug(f'Returning client {tg_id}')
        return ClientDTO(**client_dict)


    def get_by_attr(self, attr, value) -> Optional[ClientDTO]:
        logger.debug(f'Retrieving user by {attr}={value}')
        client_dict = get_single_dict_by_sql(
            self._connection,
            lambda: self._connection.execute(f"SELECT * FROM clients WHERE {attr}=?", (value,))
        )

        if client_dict is None:
            logger.debug(f'Error occurred while getting client by attr {attr}={value}')
            return None

        logger.debug(f"Returning client by {attr=}={value}")
        return ClientDTO(**client_dict)


    def get_by_state(self, state: State) -> List[ClientDTO]:
        cur = self._connection.execute(
            "SELECT * FROM clients WHERE state=?", (state,)
        )

        clients = [ClientDTO(**d) for d in cur]
        return clients


    def set_state(self, user_id, state: State):
        res = run_sql(self._connection,
                      lambda: self._connection.execute(
                          "UPDATE clients SET state=? WHERE id=?", (state.value, user_id)
                      ))
        if res is Ok:
            logger.debug(f'Client {user_id} set state to {state.value}')
        else:
            logger.error(f'Failed to set state -- {user_id}')


    def exists(self, idx: str) -> bool:
        logger.debug(f'Checking whether user exists - {idx}')
        cur = self._connection.execute("SELECT id FROM clients WHERE id=?", (idx,))
        user_dict = cur.fetchone()
        if user_dict:
            return True
        return False


    def list(self) -> List[ClientDTO]:
        raise NotImplementedError()


    def remove(self, idx) -> bool:
        logging.debug(f"Removing client with {idx=}")
        cur = self._connection.execute(
            "DELETE FROM clients WHERE id=?", (idx,)
        )
        if cur.__iter__() == 0:
            return True

        return False


    # TODO move to another db with Redis
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
