from typing import Optional, List, NoReturn

from bot.db.abstract_db import AbstractDb
from bot.models.dto.apply import ApplyDTO
from bot.static.enums.states import State


class ApplyDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        self._key_path_ = 'bot:applies'
        self.APPLY_ID_GEN = 'apply_id_gen'
        self._r_ = None

    def add(self, apply: ApplyDTO) -> bool:
        apply_id = 'apply:' + (self._r_.get(self.APPLY_ID_GEN)).decode('utf-8')
        apply.id = apply_id
        res = self._r_json_.arrappend(self._key_path_, '$', ApplyDTO.to_json_dict(apply)) is not None
        self._r_.incrby(self.APPLY_ID_GEN, 1)
        return res

    def get(self, idx: str) -> Optional[ApplyDTO]:
        res = self._r_json_.get(self._key_path_, f'$.[?(@.id=="{idx}")]')
        if len(res) == 0:
            return None

        apply_dict = res[0]
        apply = ApplyDTO.from_dict(apply_dict)
        return apply

    def set_apply_state(self, apply_id: str, state: State) -> NoReturn:
        self._r_json_.set(self._key_path_, f'$.[?(@.id="{apply_id}")].state', state.value)

    def get_by_user_id(self, user_id: str) -> List[ApplyDTO]:
        res = self._r_json_.get(self._key_path_, f'$.[?(@.user_id=={user_id})]')

        if len(res) == 0:
            return []

        applies = []
        for apply in res:
            applies.append(ApplyDTO.from_dict(apply))
        return applies

    def remove(self, idx) -> bool:
        raise NotImplemented()

    def list(self):
        raise NotImplemented()