import logging
from typing import Optional, List, NoReturn

from bot.db.abstract_db import AbstractDb
from bot.models.dto.apply import ApplyDTO
from bot.models.res import Ok
from bot.static.enums.states import State
from bot.utils import run_sql, get_single_dict_by_sql


class ApplyDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        self._table = "applies"

    def add(self, apply: ApplyDTO) -> bool:
        logging.debug(f"Adding {apply.id=}")
        res = run_sql(self._connection,
                      lambda: self._connection.execute(
                          "INSERT INTO applies (lesson_id, client_id) VALUES (?, ?)",
                          (apply.lesson_id, apply.client_id)
                      ))
        if res is Ok:
            logging.debug(f'Apply - {res.val} added')
            return True

        logging.error(f'Failed to add apply - {res.val}')
        return False

    def get(self, idx: int) -> Optional[ApplyDTO]:
        apply_dict = get_single_dict_by_sql(
            self._connection,
            lambda: self._connection.execute("SELECT * FROM applies WHERE id=?", (idx,))
        )

        if apply_dict is None:
            logging.debug(f'No apply with id={idx}')
            return None

        logging.debug(f'Returning apply {idx}')
        return ApplyDTO(**apply_dict)

    def set_apply_state(self, apply_id: int, state: State) -> NoReturn:
        res = run_sql(self._connection,
                      lambda: self._connection.execute(
                          "UPDATE applies SET state=? WHERE id=?",
                          (state.value, apply_id)
                      )
                      )
        if res is Ok:
            logging.debug(f'Apply {apply_id} set to {state.value}')

        logging.debug(f"Error occurred - {res.val}")

    def get_by_user_id(self, client_id: str) -> List[ApplyDTO]:
        res = run_sql(
            self._connection,
            lambda: self._connection.execute("SELECT * FROM applies WHERE client_id=?", (client_id,))
        )

        if res is Ok:
            apply_ds = res.val.fetchall()
            applies = [ApplyDTO(**apply_d) for apply_d in apply_ds]
            logging.debug(f'Returning applies of user {client_id}')
            return applies
        else:
            logging.debug(f'Error occurred while retrieving applies of {client_id=}')
            return []

    def remove(self, idx) -> bool:
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()
