import logging
from typing import Optional

from bot.db.abstract_db import AbstractDb
from bot.models.dto.lesson import LessonDTO


class LessonDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        self._key_path_ = 'bot:lessons'
        self.LESSON_ID_GEN = 'lesson_id_gen'
        self._r_ = None

    def add(self, lesson: LessonDTO):

        logging.debug(f'Adding lesson with {lesson.title=}...')
        lesson_id = 'lesson:' + (self._r_.get(self.LESSON_ID_GEN)).decode('utf-8')
        lesson.id = lesson_id

        res = self._r_.json().arrappend(self._key_path_, '$', LessonDTO.to_json_dict(lesson)) is not None
        logging.debug(f'Finished adding lesson with {lesson_id=}')
        self._r_.incrby(self.LESSON_ID_GEN, 1)
        return res

    def list(self):
        lessons_json_arr = self._r_json_.get(self._key_path_, '$')[0]
        lessons = [LessonDTO.from_dict(l) for l in lessons_json_arr]
        return lessons

    def get(self, idx: str) -> Optional[LessonDTO]:
        res = self._r_json_.get(self._key_path_, f'$[?(@.id=="{idx}")]')
        if len(res) == 0:
            return None

        lesson_dict = res[0]
        lesson = LessonDTO.from_dict(lesson_dict)
        return lesson

    def remove(self, idx) -> bool:
        pass