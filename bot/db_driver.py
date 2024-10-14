import logging

import redis

from bot.abstract import AbstractDb
from bot.models import LessonDTO, ApplyDTO
from bot.static.states import State

logger = logging.getLogger('main_logger')


class LessonDb(AbstractDb):
    def __init__(self, _connection_pool_):
        self.__r__ = redis.Redis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        self.LESSON_ID_GEN = 'lesson_id_gen'
        if not self.__r__.get(self.LESSON_ID_GEN):
            self.__r__.set(self.LESSON_ID_GEN, 0)

    def add(self, lesson: LessonDTO):

        logger.debug(f'Adding lesson with {lesson.title=}...')
        lesson_id = 'lesson:' + (self.__r__.get(self.LESSON_ID_GEN)).decode('utf-8')
        lesson.id = lesson_id

        res = self.__r__.json().arrappend('bot:lessons', '$', LessonDTO.to_json_dict(lesson)) is not None
        logger.debug(f'Finished adding lesson with {lesson_id=}')
        self.__r__.incrby(self.LESSON_ID_GEN, 1)
        return res

    def get_lessons(self):
        lessons_json_arr = self.__r_json__.get('bot:lessons', '$')[0]

        lessons = [LessonDTO.from_json(l) for l in lessons_json_arr]

        return lessons

    def get(self, lesson_id):
        res = self.__r_json__.get('bot:lessons', f'$.[?(@.id=="{lesson_id}")]')
        if len(res) == 0:
            return None

        lesson_dict = res[0]
        lesson = LessonDTO.from_json(lesson_dict)
        return lesson


class ApplyDb(AbstractDb):
    def __init__(self, _connection_pool_):
        self.__r__ = redis.Redis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        self.APPLY_ID_GEN = 'apply_id_gen'
        self.__r__.set(self.APPLY_ID_GEN, 0, nx=True)

    def add(self, apply: ApplyDTO):
        apply_id = 'apply:' + (self.__r__.get(self.APPLY_ID_GEN)).decode('utf-8')
        apply.id = apply_id
        res = self.__r_json__.arrappend('bot:applies', '$', ApplyDTO.to_json_dict(apply)) is not None
        self.__r__.incrby(self.APPLY_ID_GEN, 1)
        return res

    def get(self, apply_id):
        res = self.__r_json__.get('bot:applies', f'$.[?(@.id=="{apply_id}")]')
        if len(res) == 0:
            return None

        apply_dict = res[0]
        apply = ApplyDTO.from_json(apply_dict)
        return apply

    def set_apply_state(self, apply_id: str, state: State):
        self.__r_json__.set('bot:applies', f'$.[?(@.id="{apply_id}")].state', state.value)

    def get_by_user_id(self, user_id: int):
        res = self.__r_json__.get('bot:applies', f'$.[?(@.user_id=={user_id})]')

        if len(res) == 0:
            return None

        applies = []
        for apply in res:
            applies.append(ApplyDTO.from_json(apply))
        return applies
