import logging
from bot.models import LessonDAO

import redis

from bot.static.states import State

logger = logging.getLogger('main_logger')


class AdminDb:
    def __init__(self):
        logger.info('Preparing admin db driver...')

        self.__r_admin__ = redis.Redis(db=2)
        self.__r_lessons__ = redis.Redis(db=3)
        self.LESSON_ID_GEN = 'lesson_id_gen'
        # rs = __r_admin__.ft()
        if not self.__r_lessons__.get(self.LESSON_ID_GEN):
            self.__r_lessons__.set(self.LESSON_ID_GEN, 0)

        logger.info('Admin db preparing is finished')

    def user_is_admin(self, user_id):
        logger.debug(f'Checking whether {user_id} is admin')
        if self.__r_admin__.exists(user_id) > 0:
            return True
        else:
            return False

    def get_state(self, user_id) -> State:
        return State(int(self.__r_admin__.get(user_id)))

    def set_admin_state(self, user_id, state: State):
        self.__r_admin__.set(user_id, state.value)

    def add_lesson(self, lesson: LessonDAO):
        lesson_id = str(int(self.__r_lessons__.get(self.LESSON_ID_GEN), 2))
        logger.debug(f'Adding lesson with {lesson_id=}...')

        self.__r_lessons__.hset(lesson_id, mapping={
            'title': lesson.title,
            'datetime': lesson.datetime,
            'price': lesson.price,
            'description': lesson.description
        })

        logger.debug(f'Finished adding lesson with {lesson_id=}')
        self.__r_lessons__.incrby(self.LESSON_ID_GEN, 1)

    def get_lessons(self):
        lessons = []
        ids = self.__r_lessons__.scan()
        ids = ids[1][1:]
        for idx in ids:
            lesson = self.__r_lessons__.hgetall(idx)
            lesson['id'] = idx.decode('utf-8')
            lessons.append(LessonDAO.from_redis_dict(lesson))

        return lessons
