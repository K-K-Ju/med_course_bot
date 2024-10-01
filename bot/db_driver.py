import logging

import redis

from bot.utils import redis_pool
from bot.abstract import AbstractDb
from bot.models import LessonDAO, ApplyDAO
from bot.static.states import State

logger = logging.getLogger('main_logger')


class LessonDb(AbstractDb):
    def __init__(self, _connection_pool_=redis_pool):
        self.__r__ = redis.Redis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        self.LESSON_ID_GEN = 'lesson_id_gen'
        if not self.__r__.get(self.LESSON_ID_GEN):
            self.__r__.set(self.LESSON_ID_GEN, 0)

    def add(self, lesson: LessonDAO):

        logger.debug(f'Adding lesson with {lesson.title=}...')
        lesson_id = 'lesson:' + (self.__r__.get(self.LESSON_ID_GEN)).decode('utf-8')
        lesson.id = lesson_id

        res = self.__r__.json().arrappend('bot:lessons', '$.lessons', LessonDAO.to_json_dict(lesson)) is not None
        logger.debug(f'Finished adding lesson with {lesson_id=}')
        self.__r__.incrby(self.LESSON_ID_GEN, 1)
        return res

    def get_lessons(self):
        lessons_json_arr = self.__r_json__.get('bot:lessons', '$.lessons')[0]

        lessons = [LessonDAO.from_json(l) for l in lessons_json_arr]

        return lessons

    def get(self, lesson_id):
        res = self.__r_json__.get('bot:lessons', f'$.lessons[?(@.id=="{lesson_id}")]')
        if len(res) == 0:
            return None

        lesson_dict = res[0]
        lesson = LessonDAO.from_json(lesson_dict)
        return lesson


class ApplyDb(AbstractDb):
    def __init__(self, _connection_pool_=redis_pool):
        self.__r__ = redis.Redis(connection_pool=_connection_pool_)
        self.__r_json__ = self.__r__.json()
        self.APPLY_ID_GEN = 'apply_id_gen'
        self.__r__.set(self.APPLY_ID_GEN, 0, nx=True)

    def add(self, apply: ApplyDAO):
        apply_id = 'apply:' + (self.__r__.get(self.APPLY_ID_GEN)).decode('utf-8')
        apply.id = apply_id
        res = self.__r_json__.arrappend('bot:applies', '$.applies', ApplyDAO.to_json_dict(apply)) is not None
        self.__r__.incrby(self.APPLY_ID_GEN, 1)
        return res

    def get(self, apply_id):
        res = self.__r_json__.get('bot:applies', f'$.applies[?(@.id=="{apply_id}")]')
        if len(res) == 0:
            return None

        apply_dict = res[0]
        apply = ApplyDAO.from_json(apply_dict)
        return apply

    def set_apply_state(self, apply_id: str, state: State):
        self.__r_json__.set('bot:applies', f'$.applies[?(@.id="{apply_id}")].state', state.value)
