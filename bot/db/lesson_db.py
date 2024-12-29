import logging
from typing import Optional, NoReturn, List

from bot.db.abstract_db import AbstractDb
from bot.models.dto.lesson import LessonDTO
from bot.models.res import Ok
from bot.utils import run_sql, get_single_dict_by_sql


class LessonDb(AbstractDb):
    def __init__(self, connection):
        super().__init__(connection)
        self._table = "lessons"

    def add(self, lesson: LessonDTO) -> NoReturn:
        logging.debug(f'Adding lesson with {lesson.idx=}...')
        res = run_sql(self._connection,
                      lambda: self._connection.execute(
                          "INSERT INTO lessons (title, datetime, price, description)  VALUES (?, ?, ?, ?)",
                          (lesson.title, lesson.datetime, lesson.price, lesson.description)
                      ))
        if res is Ok:
            logging.debug(f'Lesson {res.val} added')
        else:
            logging.error(f'Failed to add lesson -- {lesson=}')

    def list(self) -> List[LessonDTO]:
        cur = self._connection.execute("SELECT * FROM lessons")
        lessons_ds = cur.fetchall()
        lessons = [LessonDTO(**lesson_d) for lesson_d in lessons_ds]
        logging.debug("Returning all lessons")
        return lessons

    def get(self, idx: int) -> Optional[LessonDTO]:
        lesson_dict = get_single_dict_by_sql(
            self._connection,
            lambda: self._connection.execute("SELECT * FROM lessons WHERE id=?", (idx,))

        )
        if lesson_dict is None:
            logging.debug(f"No lesson with {idx=}")
            return None

        logging.debug(f"Returning lesson {idx}")
        return LessonDTO(**lesson_dict)


    def remove(self, idx) -> bool:
        pass
