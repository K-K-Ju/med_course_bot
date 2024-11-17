import logging
from typing import List, NoReturn, Optional

import redis

from bot.abstract import AbstractDb
from bot.models import LessonDTO, ApplyDTO
from bot.static.states import State

logger = logging.getLogger('main_logger')


class LessonDb(AbstractDb):
    def __init__(self, _connection_pool_):
        self._key_path_ = 'bot:lessons'
        self._r_ = redis.Redis(connection_pool=_connection_pool_)
        self._r_json_ = self._r_.json()
        self.LESSON_ID_GEN = 'lesson_id_gen'
        self._r_.set(self.LESSON_ID_GEN, 0, nx=True)

    def add(self, lesson: LessonDTO):

        logger.debug(f'Adding lesson with {lesson.title=}...')
        lesson_id = 'lesson:' + (self._r_.get(self.LESSON_ID_GEN)).decode('utf-8')
        lesson.id = lesson_id

        res = self._r_.json().arrappend(self._key_path_, '$', LessonDTO.to_json_dict(lesson)) is not None
        logger.debug(f'Finished adding lesson with {lesson_id=}')
        self._r_.incrby(self.LESSON_ID_GEN, 1)
        return res

    def list(self):
        lessons_json_arr = self._r_json_.get(self._key_path_, '$')[0]
        lessons = [LessonDTO.from_json(l) for l in lessons_json_arr]
        return lessons

    def get(self, idx: str) -> Optional[LessonDTO]:
        res = self._r_json_.get(self._key_path_, f'$[?(@.id=="{idx}")]')
        if len(res) == 0:
            return None

        lesson_dict = res[0]
        lesson = LessonDTO.from_json(lesson_dict)
        return lesson

    def remove(self, idx) -> bool:
        pass


class ApplyDb(AbstractDb):
    def __init__(self, _connection_pool_):
        self._r_ = redis.Redis(connection_pool=_connection_pool_)
        self._key_path_ = 'bot:applies'
        self._r_json_ = self._r_.json()
        self.APPLY_ID_GEN = 'apply_id_gen'
        self._r_.set(self.APPLY_ID_GEN, 0, nx=True)

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
        apply = ApplyDTO.from_json(apply_dict)
        return apply

    def set_apply_state(self, apply_id: str, state: State) -> NoReturn:
        self._r_json_.set(self._key_path_, f'$.[?(@.id="{apply_id}")].state', state.value)

    def get_by_user_id(self, user_id: str) -> List[ApplyDTO]:
        res = self._r_json_.get(self._key_path_, f'$.[?(@.user_id=={user_id})]')

        if len(res) == 0:
            return []

        applies = []
        for apply in res:
            applies.append(ApplyDTO.from_json(apply))
        return applies

    def remove(self, idx) -> bool:
        raise NotImplemented()

    def list(self):
        raise NotImplemented()
